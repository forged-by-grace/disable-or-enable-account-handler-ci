from passlib.context import CryptContext

from core.event.produce_event import produce_event

from core.utils.settings import settings
from core.model.update_model import UpdateAvro, UpdateFieldAvro

from datetime import datetime
from core.utils.init_log import logger


async def disable_or_enable_account(account_data) -> None:
    # Create delete account obj
    disable_account_obj = UpdateFieldAvro(action='$set', value={'disabled': account_data.disabled})
    last_update = UpdateFieldAvro(action='$set', value={'last_update': datetime.utcnow().isoformat()})

    # Create update obj
    update_obj = UpdateAvro(
            db_metadata={'provider': 'mongoDB', 
                        'database': 'account_db', 
                        'collection': 'accounts'},
            db_filter={'_id': account_data.id}, 
            updates=[disable_account_obj, last_update]
        )
   
    # Serialize
    delete_account_event = update_obj.serialize()

    # Emit event
    logger.info('Emitting db event.')
    await produce_event(topic=settings.api_update_account_topic, value=delete_account_event)
    
