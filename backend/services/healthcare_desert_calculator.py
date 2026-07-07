"""
Healthcare Desert Calculator Service

Calculates healthcare necessity scores for regions based on:
- Distance to nearest clinic
- Number of health sites in region
- Specialist availability
- Transportation difficulty (season-adjusted)

Higher score = greater need for telehealth (0-100 scale)
"""
import math
from typing import Dict, Optional, Tuple, List, Union
from sqlalchemy.orm import Session
from database.models import HealthcareSite, CATRegion, CATDataPoint
from services.season_constants import (
    SEASON_SUMMER, SEASON_WINTER, SEASON_YEAR_ROUND, VALID_SEASONS,
    ROAD_QUALITY_LOCAL, VALID_ROAD_QUALITIES,
    get_seasonal_modifier, get_road_friction, get_season_display_name
)


class HealthcareDesertCalculator:
    """
    Calculate healthcare desert metrics for CAT regions.
    
    Necessity score ranges from 0-100:
    - 0-30: Good healthcare access
    - 31-50: Moderate access challenges
    - 51-70: Significant healthcare desert
    - 71-100: Severe healthcare desert - high telehealth priority
    """
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate haversine distance in km"""
        R = 6371  # Earth radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c

    @staticmethod
    def score_distance_component(distance_km: float) -> float:
        """Normalize distance to nearest facility: 0km=0, 300+km=100."""
        return min(100, (max(distance_km, 0) / 300) * 100)

    @staticmethod
    def score_density_component(num_sites: int) -> float:
        """Score facility density. Fewer facilities means higher need."""
        if num_sites <= 0:
            return 100
        if num_sites == 1:
            return 70
        if num_sites == 2:
            return 40
        return 10

    @staticmethod
    def score_specialist_component(has_specialists: bool) -> float:
        """Score specialist access. No specialists means higher need."""
        return 0 if has_specialists else 100

    @staticmethod
    def score_transport_component(
        travel_time_minutes: Optional[float],
        season: str = SEASON_YEAR_ROUND,
        road_quality: str = ROAD_QUALITY_LOCAL,
        transport_mode: str = "road",
    ) -> float:
        """Score seasonal transport difficulty on a 0-100 scale."""
        if season not in VALID_SEASONS:
            season = SEASON_YEAR_ROUND
        if road_quality not in VALID_ROAD_QUALITIES:
            road_quality = ROAD_QUALITY_LOCAL

        if not travel_time_minutes:
            if season == SEASON_WINTER:
                return 70
            if season == SEASON_SUMMER:
                return 40
            return 50

        mode = transport_mode if transport_mode in {"road", "water", "air"} else "road"
        friction = get_road_friction(road_quality, season) if mode == "road" else 1.0
        adjusted_travel_time = travel_time_minutes * friction

        modifier = get_seasonal_modifier(mode, season, road_quality)
        if modifier < 0.1:
            return 100

        availability_penalty = (1.0 - modifier) * 30
        base_transport_score = min(100, (adjusted_travel_time / 240) * 100)
        return min(100, base_transport_score + availability_penalty)

    @staticmethod
    def _region_center(db: Session, region_code: str) -> Optional[Tuple[float, float]]:
        region = db.query(CATRegion).filter(
            CATRegion.region_code == region_code
        ).first()

        if not region:
            return None

        data_points = db.query(CATDataPoint).filter(
            CATDataPoint.region_code == region_code
        ).all()

        if data_points:
            avg_lat = sum(p.latitude for p in data_points) / len(data_points)
            avg_lon = sum(p.longitude for p in data_points) / len(data_points)
            return avg_lat, avg_lon

        if region.centroid_lat is not None and region.centroid_lon is not None:
            return region.centroid_lat, region.centroid_lon

        return None
    
    @staticmethod
    def calculate_healthcare_necessity_score(
        db: Session, 
        region_or_code: Union[str, CATRegion],
        season: str = SEASON_YEAR_ROUND,
        road_quality: str = ROAD_QUALITY_LOCAL
    ) -> Dict:
        """
        Calculate compound healthcare desert metric (0-100).
        Higher score = greater need for telehealth.
        """
        if isinstance(region_or_code, str):
            region = db.query(CATRegion).filter(CATRegion.region_code == region_or_code).first()
            if not region:
                region = CATRegion(region_code=region_or_code)
        else:
            region = region_or_code
            
        # 1. Distance factor (0-100) incorporates both clinic and hospital
        clinic_dist = region.nearest_clinic_km if region.nearest_clinic_km is not None else 500.0
        hospital_dist = region.nearest_hospital_km if region.nearest_hospital_km is not None else 500.0
            
        # Normalize: 0km=0 points, 300+km=100 points for clinic
        clinic_score = HealthcareDesertCalculator.score_distance_component(clinic_dist)
        # Hospital distance is more vital, scales over 500km
        hospital_score = min(100.0, (hospital_dist / 500.0) * 100.0)
        
        # Strong penalty for lacking hospital access
        distance_score = (0.6 * hospital_score) + (0.4 * clinic_score)
        
        # 2. Health site density (0-100)
        num_sites = region.healthcare_density if region.healthcare_density is not None else 0
        density_score = HealthcareDesertCalculator.score_density_component(num_sites)
        
        # 3. Specialist availability (0-100)
        has_specialists = region.has_specialist if region.has_specialist is not None else False
        specialist_score = HealthcareDesertCalculator.score_specialist_component(has_specialists)
        
        # Validate season and road_quality inputs
        if season not in VALID_SEASONS:
            season = SEASON_YEAR_ROUND
        if road_quality not in VALID_ROAD_QUALITIES:
            road_quality = ROAD_QUALITY_LOCAL
        
        # 4. Transportation difficulty (0-100) - SEASON ADJUSTED
        data_point = db.query(CATDataPoint).filter(
            CATDataPoint.region_code == region.region_code
        ).first()
        
        transport_score = HealthcareDesertCalculator.score_transport_component(
            data_point.travel_time_minutes if data_point else None,
            season,
            road_quality,
            "road",
        )
        
        # Calculate weighted score
        necessity_score = float(
            0.50 * distance_score +
            0.15 * density_score +
            0.15 * specialist_score +
            0.20 * transport_score
        )
        
        nearest_dist = min(clinic_dist, hospital_dist)
        
        return {
            'necessity_score': round(necessity_score, 2),
            'distance_to_nearest_clinic_km': round(float(clinic_dist), 2),
            'distance_to_nearest_hospital_km': round(float(hospital_dist), 2),
            'distance_to_nearest_facility_km': round(float(nearest_dist), 2),
            'num_healthcare_sites': num_sites,
            'has_specialist_access': has_specialists,
            'avg_travel_time_minutes': data_point.travel_time_minutes if data_point else None,
            'season_scenario': {
                'active_season': season,
                'season_display': get_season_display_name(season),
                'road_quality': road_quality,
                'assumption': 'User-selected seasonal scenario for planning purposes. '
                             'Actual conditions may vary.'
            },
            'breakdown': {
                'distance_component': round(float(distance_score), 2),
                'density_component': round(float(density_score), 2),
                'specialist_component': round(float(specialist_score), 2),
                'transport_component': round(float(transport_score), 2),
                'transport_season_adjusted': True
            }
        }
    
    @staticmethod
    def get_all_region_scores(
        db: Session,
        season: str = SEASON_YEAR_ROUND,
        road_quality: str = ROAD_QUALITY_LOCAL,
        page: int = 1,
        limit: int = 50
    ) -> Dict:
        """
        Get necessity scores for all regions, paginated and sorted by score.
        """
        query = db.query(CATRegion)
        total = query.count()
        
        regions = query.offset((page - 1) * limit).limit(limit).all()
        
        results = []
        for region in regions:
            score_data = HealthcareDesertCalculator.calculate_healthcare_necessity_score(
                db, region, season, road_quality
            )
            results.append({
                'region_code': region.region_code,
                'region_name': region.region_name,
                'tier_level': region.tier_level,
                'cat_tier': region.tier_level,
                'necessity_score': score_data['necessity_score'],
                'num_healthcare_sites': score_data['num_healthcare_sites'],
                'has_specialist_access': score_data['has_specialist_access'],
                'season_applied': season,
                'components': score_data['breakdown'],
                'is_telehealth_priority': score_data['necessity_score'] > 75.0,
                'risk_level': 'critical' if score_data['necessity_score'] > 85.0 else 'high' if score_data['necessity_score'] > 70.0 else 'moderate'
            })
            
        # Sort by necessity score (highest first)
        results.sort(key=lambda x: x['necessity_score'], reverse=True)
        
        return {
            "data": results,
            "meta": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": math.ceil(total / limit) if limit > 0 else 1
            }
        }


    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        if None in (lat1, lon1, lat2, lon2):
            return float('inf')
            
        # Convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

        # Haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 
        r = 6371 # Radius of earth in kilometers
        return c * r

# Module-level convenience wrapper so callers don't need to import the class.
def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Haversine distance in km. Delegates to HealthcareDesertCalculator.calculate_distance."""
    return HealthcareDesertCalculator.calculate_distance(lat1, lon1, lat2, lon2)
