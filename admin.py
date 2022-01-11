from PhongKhamTu import db, app
from PhongKhamTu.model import *
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, Admin
from flask_login import current_user, logout_user
from flask import redirect, request
from flask_admin import AdminIndexView
from datetime import datetime
import utils

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class MedicineView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {'id': 'Mã Thuốc', 'name': 'Tên thuốc', 'price': 'Gía tiền', 'unit': 'Đơn vị'}
    column_filters = ['name', 'price']
    column_searchable_list = ['name']

class MedicalCertificateView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {"id": 'Mã Phiếu Khám','doctor_id': 'Mã bác sĩ', 'healthcheck_date': 'Ngày khám', 'symptom': 'Triệu chứng', 'guess': 'Dự đoán bệnh', 'patient_id': 'Bệnh nhân'}
    column_filters = ['doctor_id', 'healthcheck_date', 'patient_id']
    column_searchable_list = ['doctor_id']
    column_exclude_list = ['patient']

class PATIENTView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {"id": 'Mã Bệnh Nhân','name': 'Tên Bệnh Nhân', 'yearofbirth': 'Năm sinh', 'address': 'Địa chỉ'}
    column_searchable_list = ['name','yearofbirth', 'address']
    edit_modal = True
    details_modal = True
    create_modal = True

class BillView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = ({"id": 'Mã Hóa Đơn', 'nurse_id': "Mã Y Tá", 'healthCheck_price': 'Tiền Khám'})
    column_exclude_list = ['medicalcertificate']

class MedicalCertificateDetailView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {'quantily': 'Số Lượng', 'medicine': 'Tên Thuốc', 'medicalcertificate': 'Mã Phiếu Khám'}

class UnitView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {'name': 'Đơn Vị', 'id': 'Mã Đơn Vị'}

class MesicalRView(AuthenticatedModelView):
    can_view_details = True
    can_export = True

class UserView(AuthenticatedModelView):
    can_view_details = True

class MedicalExaminationPatientView(AuthenticatedModelView):
    can_view_details = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_labels = {'patient': 'Tên Bệnh Nhân', 'medicalexaminationlist':'Danh Sách Khám Bệnh'}
    column_searchable_list = ['mc_id']

class MedicalExaminationListView(AuthenticatedModelView):
    edit_modal = True
    details_modal = True
    create_modal = True
    column_labels = {"id": 'Mã Phiếu Khám','nurse_id': "Mã Y Tá" , 'mc_date': 'Ngày Khám Bệnh'}
    column_display_pk = True
    can_view_details = True
    can_export = True

class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html', stats=utils.drugfrequency_stats())

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        kwtt = request.args.get('kwtt')
        kwdv = request.args.get('kwdv')
        kwsld = request.args.get('sl')
        kwname = request.args.get('kwname')
        kwy = request.args.get('kwy')
        kwslk = request.args.get('kwslk')
        kwds = request.args.get('kwds')
        kwyt = request.args.get('kwyt')
        kwbn = request.args.get('kwbn')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        return self.render('admin/index.html', stats=utils.drugfrequency_stats(kwtt=kwtt, kwdv=kwdv, kwsld=kwsld),patient = utils.patient_view(kwname=kwname, kwy=kwy, kwslk=kwslk), mclist = utils.mclist_view(kwds=kwds, kwyt=kwyt,kwbn=kwbn, from_date=from_date, to_date=to_date))



admin = Admin(app=app, name='Phong Kham Tu', template_mode='bootstrap4', index_view=MyAdminIndexView())

admin.add_view(MedicalCertificateView(MedicalCertificate, db.session, name='Phiếu Khám'))
admin.add_view(MedicineView(Medicine, db.session, name='Danh Sách Thuốc'))
admin.add_view(BillView(Bill, db.session, name='Hóa Đơn'))
admin.add_view(PATIENTView(PATIENT, db.session, name='Bệnh Nhân'))
admin.add_view(MedicalCertificateDetailView(MedicalCertificateDetail, db.session, name='Thêm Thuốc Vào Phiếu khám'))
admin.add_view(UnitView(Unit, db.session, name='Đơn Vị'))
admin.add_view(UserView(User, db.session, name='User'))
admin.add_view(MesicalRView(MedicalRegister, db.session))
admin.add_view(MedicalExaminationPatientView(MedicalExaminationPatient, db.session, name ='Bệnh Nhân Khám Bệnh'))
admin.add_view(MedicalExaminationListView(MedicalExaminationList, db.session, name='Danh Sách Khám Bệnh'))
admin.add_view(StatsView(name='Thống Kê'))
admin.add_view(LogoutView(name='Đăng Xuất'))