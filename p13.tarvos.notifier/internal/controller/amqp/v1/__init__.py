from pkg.rabbitmq.rpc import RPCRouter

from . import mail


router = RPCRouter()
router.include_router(
    mail.router,
    prefix='/mail',
)
