import datetime
from ninja import NinjaAPI


from ninja_extra import NinjaExtraAPI

from ninja_jwt.controller import NinjaJWTDefaultController


from cpc.api import router as cpc_router
from economic_analysis.data_tools.points_awarded import read_points_awardeds
from reports.api import router as reports_router

from shares.api import router as shares_router

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)


@api.get("/hello")
def hello(request):
    # read_points_awardeds(
    #     file_path="/Users/kevincoder/Desktop/data/InvestList202411242.csv",
    #     shopid="319134",
    # )
    return {"message": "Hello World!"}


api.add_router("/cpc", cpc_router)
api.add_router("/share", shares_router)
api.add_router("/reports", reports_router)
