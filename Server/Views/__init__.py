from flask import Blueprint
from flask_restful import Api

api_endpoint = Blueprint

from Server.Views.userview import CountUsers, AddUser,UserLogin,UserResourcesById
from Server.Views.providerviews import CountProviders, ViewALLProviders,AddProvider,GetSingleProvider
from Server.Views.reviews import AddReviews,GetReviewsForProvider,GetAllReviews
from Server.Views.individualdoctorviews import AddIndividualDoctor, GetIndividualDoctorDetails
from Server.Views.facilityviews import AddFacilities,GetFacilityForProvider
from Server.Views.getproviderviews import GetProviders
from Server.Views.additionaluserinfo import AdditionalUserInfoResource,USerInfo
from Server.Views.providersdashbord import SpecificUserProvider
from Server.Views.superAdmin import UsersList,UpdateUserrole,ProvidersList,UnpublishedProviders,ApproveProvider

api_endpoint= Blueprint('auth',__name__,url_prefix='/care')
api = Api(api_endpoint)


api.add_resource(CountUsers, '/countusers')
api.add_resource(AddUser, '/addusers')
api.add_resource(UserLogin,'/login')
api.add_resource(UserResourcesById, '/users/<int:user_id>')

api.add_resource(CountProviders, '/totalproviders')
api.add_resource(ViewALLProviders, '/providers') ## not working fix
api.add_resource(AddProvider,'/newprovider')
api.add_resource(GetSingleProvider,'/provider/<int:providerID>')
#missing endpoint get single provider

api.add_resource(AddReviews, '/newreview/<int:providerID>')
api.add_resource(GetReviewsForProvider, '/reviews/<int:providerID>')
api.add_resource(GetAllReviews, '/allreviews')

api.add_resource(AddIndividualDoctor, '/newdoctor')
api.add_resource(GetIndividualDoctorDetails,'/doctor/<int:providerID>')

api.add_resource(AddFacilities,'/newfacility')
api.add_resource(GetFacilityForProvider,'/facility/<int:providerID>')

api.add_resource(GetProviders, '/allproviders')

api.add_resource(AdditionalUserInfoResource, '/newuserinfo')
api.add_resource(USerInfo, '/userinfo/<int:id>')

api.add_resource(SpecificUserProvider, '/admin')

api.add_resource(UsersList, '/super-admin')
api.add_resource(UpdateUserrole, '/user/<int:user_id>')
api.add_resource(ProvidersList, '/super-admin-allproviders')
api.add_resource(UnpublishedProviders, '/super-admin-unapproved')
api.add_resource(ApproveProvider, '/approve_provider/<int:providerID>')


