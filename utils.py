import os
from PhongKhamTu import app, db
from PhongKhamTu.model import *
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import extract
import hashlib


def get_user_by_id(user_id):
    return User.query.get(user_id)

def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()

def check_admin(username, password, role):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()

def drugfrequency_stats(kwtt=None, kwdv=None, kwsld=None):
    p = db.session.query(Medicine.name, Unit.name, func.sum(MedicalCertificateDetail.quantily), func.count(MedicalCertificateDetail.medicine_id))\
    .join(Unit)\
    .join(MedicalCertificateDetail, MedicalCertificateDetail.medicine_id.__eq__(Medicine.id), isouter=True)\
    .join(MedicalCertificate, MedicalCertificate.id.__eq__(MedicalCertificateDetail.mc_id))\
    .group_by(Medicine.id, Medicine.name)

    if kwtt:
        p = p.filter(Medicine.name.contains((kwtt)))
    if kwdv:
        p = p.filter(Unit.name.contains(kwdv))
    if kwsld:
        p = p.filter(func.count(MedicalCertificateDetail.medicine_id).__eq__(kwsld))

    return p.all()

def mclist_view(kwds = None, kwyt = None,kwbn =None, from_date = None, to_date = None):
    p = db.session.query(MedicalExaminationList.id, MedicalExaminationList.nurse_id,\
                         MedicalExaminationList.mc_date, MedicalExaminationPatient.patient_id, PATIENT.name)\
        .join(MedicalExaminationPatient, MedicalExaminationPatient.mc_id.__eq__(MedicalExaminationList.id), isouter = True)\
        .join(PATIENT, PATIENT.id.__eq__(MedicalExaminationPatient.patient_id))\
        .group_by(MedicalExaminationList.id, MedicalExaminationList.nurse_id,\
                    MedicalExaminationList.mc_date, MedicalExaminationPatient.patient_id, PATIENT.name)

    if kwds:
        p = p.filter(MedicalExaminationList.id.__eq__(kwds))
    if kwyt:
        p = p.filter(MedicalExaminationList.nurse_id.__eq__(kwyt))
    if kwbn:
        p = p.filter(PATIENT.id.__eq__(kwbn))
    if from_date:
        p = p.filter(MedicalExaminationList.mc_date.__ge__(from_date))
    if to_date:
        p = p.filter(MedicalExaminationList.mc_date.__le__(to_date))

    return p.all()

def patient_view(kwname =None, kwy = None, kwslk = None):
    p = db.session.query(PATIENT.id, PATIENT.name,PATIENT.yearofbirth, func.count(MedicalExaminationPatient.mc_id))\
                        .join(MedicalExaminationPatient, MedicalExaminationPatient.patient_id.__eq__(PATIENT.id), isouter = True)\
                        .group_by(PATIENT.id, PATIENT.name,PATIENT.yearofbirth)

    if kwname:
        p = p.filter(PATIENT.name.contains(kwname))
    if kwy:
        p = p.filter(PATIENT.yearofbirth.__eq__(kwy))
    if kwslk:
        pass
    return p.all()


def count_patient_in_day(registerdate):
    return MedicalRegister.query.filter(MedicalRegister.register_date == registerdate).count()

def add_register(name, birth, address, c_id, phone, gt):
    p = PATIENT(name = name
                , yearofbirth = birth
                , address = address,
                citizen_identification = c_id,
                gioitinh = gt,
                phone = phone)
    db.session.add(p)
    db.session.commit()

def add_user(name, username, password,birth, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name = name,username=username,password=password,
                yearofbirth = birth,
                email = kwargs.get('email'),avatar = kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def get_patient_by_Cid(c_id):
    p = PATIENT.query.filter(PATIENT.citizen_identification.__eq__(c_id)).first();
    return p


def add_patient_register(p_id, register_date):
    mg = MedicalRegister(patient_id = p_id, register_date = register_date)
    db.session.add(mg)
    db.session.commit()

def get_patient_by_day(registerdate):
    p = db.session.query(PATIENT.id, PATIENT.name, PATIENT.yearofbirth, PATIENT.gioitinh, PATIENT.address, MedicalRegister.register_date).\
        join(MedicalRegister, MedicalRegister.patient_id.__eq__(PATIENT.id), isouter = True).\
        group_by(PATIENT.id, PATIENT.name, PATIENT.yearofbirth, PATIENT.gioitinh, PATIENT.address, MedicalRegister.register_date)
    if registerdate:
        p = p.filter(MedicalRegister.register_date == registerdate)
    return p.all()

def add_MedicalExaminationList(note):
    if note:
        for i in note.values():
            ngay = i['ngay']
            break;

        MEL = MedicalExaminationList(user = current_user, mc_date = ngay)
        db.session.add(MEL)

        for n in note.values():
            d = MedicalExaminationPatient(medicalexaminationlist = MEL, patient_id = n['id'])
            db.session.add(d)

        db.session.commit()


def read_Medicalcertificate():
    return MedicalCertificate.query.all()

def get_mc_by_id(pk_id):
    p = db.session.query(MedicalCertificate.healthcheck_date, PATIENT.name).\
        join(PATIENT, PATIENT.id.__eq__(MedicalCertificate.patient_id),  isouter = True).\
        group_by(MedicalCertificate.healthcheck_date, PATIENT.name)
    if(pk_id):
        p = p.filter(MedicalCertificate.id.__eq__(pk_id))
    return p.all()
def get_tienkham():
    return Regulation.query.get(1)

def tienthuoc(pk_id = None):
    p = db.session.query(Medicine.price, MedicalCertificateDetail.quantily).\
        join(Medicine, Medicine.id.__eq__(MedicalCertificateDetail.medicine_id), isouter = True).\
        group_by(Medicine.price, MedicalCertificateDetail.quantily)
    if pk_id:
        p = p.filter(MedicalCertificateDetail.mc_id.__eq__(pk_id))
    return p.all()
def add_bill(mc_id = None, tk = None):
    if mc_id:
      b = Bill(mc_id = mc_id, healthCheck_price = tk)
      db.session.add(b)
    db.session.commit()


