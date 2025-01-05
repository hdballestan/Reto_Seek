from copy import deepcopy

# Pipeline de agregación para calcular el precio promedio
BASE_PIPELINE = [
    {
        "$match": {
            "published_date": {
                "$gte": None,  # Se rellenará dinámicamente
                "$lt": None   # Se rellenará dinámicamente
            }
        }
    },
    {
        "$group": {
            "_id": {"$year": "$published_date"},
            "avg_price": {"$avg": {"$toDouble": "$price"}}
        }
    },
    {
        "$project": {
            "_id": 0,
            "year": "$_id",
            "avg_price": 1
        }
    },
    {
        "$sort": {"year": 1}
    }
]

def get_pipeline(start_date, end_date):
    """
    Devuelve una copia del pipeline con las fechas dinámicas configuradas.
    
    :param start_date: Fecha de inicio (datetime).
    :param end_date: Fecha de fin (datetime).
    :return: Lista del pipeline configurada.
    """
    pipeline = deepcopy(BASE_PIPELINE)
    pipeline[0]["$match"]["published_date"]["$gte"] = start_date
    pipeline[0]["$match"]["published_date"]["$lt"] = end_date
    return pipeline
