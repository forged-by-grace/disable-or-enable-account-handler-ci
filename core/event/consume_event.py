from core.helper.consumer_helper import consume_event
from core.model.account_model import Disable_Enable_Account
from core.utils.settings import settings
from core.helper.account_helper import disable_or_enable_account
from core.utils.init_log import logger


async def consume_disable_or_enable_account_event():
    # consume event
    consumer = await consume_event(topic=settings.api_disable_enable_account_topic, group_id=settings.api_disable_enable_account_topic)
    
    try:
        # Consume messages
        async for msg in consumer:  
            logger.info('Received disable or enable account event.')          
            
            # Deserialize event
            account_data = Disable_Enable_Account.deserialize(data=msg.value)

            # Processing event
            logger.info('Processing event.')
            await disable_or_enable_account(account_data)
            
    except Exception as err:
        logger.error(f'Failed to process event with error: {str(err)}')
    finally:
        logger.warning('Consumer is stopping.')
        await consumer.stop()
