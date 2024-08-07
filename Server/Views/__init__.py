from flask import Blueprint
from flask_restful import Api

api_endpoint = Blueprint

from Server.Views.userview import CountUsers, AddUser,UserLogin,UserResourcesById,SendEmail
from Server.Views.providerviews import CountProviders, ViewALLProviders,AddProvider,GetSingleProvider,GetDoctorProviders,GetFacilityProviders
from Server.Views.reviews import AddReviews,GetReviewsForProvider,GetAllReviews
from Server.Views.individualdoctorviews import AddIndividualDoctor, GetIndividualDoctorDetails
from Server.Views.facilityviews import AddFacilities,GetFacilityForProvider
from Server.Views.getproviderviews import GetProviders
from Server.Views.additionaluserinfo import AdditionalUserInfoResource,USerInfo
from Server.Views.providersdashbord import SpecificUserProvider,GrantAdminAccess
from Server.Views.superAdmin import UsersList,UpdateUserrole,ProvidersList,UnpublishedProviders,ApproveProvider

api_endpoint= Blueprint('auth',__name__,url_prefix='/care')
api = Api(api_endpoint)


api.add_resource(CountUsers, '/countusers')
api.add_resource(AddUser, '/addusers')
api.add_resource(UserLogin,'/login')
api.add_resource(UserResourcesById, '/users/<int:user_id>')
api.add_resource(SendEmail, '/send')

api.add_resource(CountProviders, '/totalproviders')
api.add_resource(ViewALLProviders, '/providers') 
api.add_resource(AddProvider,'/newprovider')
api.add_resource(GetSingleProvider,'/provider/<int:providerID>')
api.add_resource(GetDoctorProviders, '/provider/doctors')
api.add_resource(GetFacilityProviders, '/provider/facility')
#missing endpoint get single provider

api.add_resource(AddReviews, '/newreview/<int:providerID>')
api.add_resource(GetReviewsForProvider, '/reviews/<int:providerID>')
api.add_resource(GetAllReviews, '/allreviews')

api.add_resource(AddIndividualDoctor, '/newdoctor')
api.add_resource(GetIndividualDoctorDetails,'/doctor/<int:providerID>')

api.add_resource(AddFacilities,'/newfacility')
api.add_resource(GetFacilityForProvider,'/facility/<int:providerID>')

api.add_resource(GetProviders, '/foryoupage')

api.add_resource(AdditionalUserInfoResource, '/newuserinfo')
api.add_resource(USerInfo, '/userinfo/<int:id>')

api.add_resource(SpecificUserProvider, '/admin')

api.add_resource(UsersList, '/superadmin/users')
api.add_resource(UpdateUserrole, '/superadmin/user/<int:user_id>')
api.add_resource(ProvidersList, '/superadmin/providers')
api.add_resource(UnpublishedProviders, '/superadmin/providers/unapproved')
api.add_resource(ApproveProvider, '/superadmin/aproveprovider/<int:providerID>')
api.add_resource(GrantAdminAccess, '/grant-admin-access')


