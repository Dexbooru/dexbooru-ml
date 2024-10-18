from fastapi import APIRouter

def register_endpoints(router: APIRouter):
    @router.get('/health-check')
    def health_check():
        return {'status': 'healthy'}

def build_general_router() -> tuple[APIRouter, str]:
    router = APIRouter()
    register_endpoints(router)

    return router, 'general'