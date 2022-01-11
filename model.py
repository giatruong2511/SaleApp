from PhongKhamTu import db
from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from flask_login import UserMixin
from enum import Enum as UserEnum


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    PATIENT = 1
    DOCTOR = 2
    NURSE = 3
    ADMIN = 4


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    yearofbirth = Column(Integer, nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default= date.today())
    user_role = Column(Enum(UserRole), default=UserRole.PATIENT)
    MEL = relationship('MedicalExaminationList', backref='user', lazy = True)
    def __str__(self):
        return self.name


class PATIENT(BaseModel):
    __tablename__ = 'patient'
    name = Column(String(50), nullable=False)
    yearofbirth = Column(Integer, nullable=False)
    phone = Column(String(10))
    gioitinh = Column(String(10), nullable=False)
    address = Column(String(100))
    citizen_identification = Column(String(13), nullable=False)
    patientMEP = relationship('MedicalExaminationPatient', backref='patient', lazy=True)
    patientMC = relationship('MedicalCertificate', backref='patient', lazy=True)
    patientMR = relationship('MedicalRegister', backref='patient', lazy=True)
    def __str__(self):
        return self.name


# QuyDinh
class Regulation(BaseModel):
    __tablename__ = 'regulations'
    name = Column(String(50), nullable=False)
    value = Column(Integer)
    def __str__(self):
        return self.name


# DonVi
class Unit(BaseModel):
    __tablename__ = 'unit'
    name = Column(String(50), nullable=False)
    units = relationship('Medicine', backref='unit', lazy=True)

    def __str__(self):
        return self.name


# Thuoc
class Medicine(BaseModel):
    __tablename__ = 'medicine'
    name = Column(String(50), nullable=False)
    unit_id = Column(Integer, ForeignKey(Unit.id), nullable=False)
    price = Column(Float, default=0)
    mc_details = relationship('MedicalCertificateDetail', backref='medicine', lazy=True)

    def __str__(self):
        return self.name

    # Phieu Kham
class MedicalCertificate(BaseModel):
    __tablename__ = 'medicalcertificate'
    doctor_id = Column(Integer)
    patient_id = Column(Integer, ForeignKey(PATIENT.id), nullable=False)
    healthcheck_date = Column(DateTime, default=date.today())
    symptom = Column(String(100))
    guess = Column(String(100))
    details = relationship('MedicalCertificateDetail', backref='medicalcertificate', lazy=True)
    bills = relationship('Bill', backref='medicalcertificate', lazy=True)


# PhieuKham_Thuoc
class MedicalCertificateDetail(db.Model):
    __tablename__ = 'medicalcertìicatedetail'
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False, primary_key=True)
    mc_id = Column(Integer, ForeignKey(MedicalCertificate.id), nullable=False, primary_key=True)
    quantily = Column(Float, default=1)
    user_manual = Column(String(500), nullable=False)

# HoaDon
class Bill(BaseModel):
    __tablename__ = 'bill'
    mc_id = Column(Integer, ForeignKey(MedicalCertificate.id), nullable=False)
    nurse_id = Column(Integer)
    healthCheck_price = Column(Float, nullable= False)


# DanhSachKhamBenh
class MedicalExaminationList(BaseModel):
    __tablename__ = 'medicalexaminationlist'
    nurse_id = Column(Integer,ForeignKey(User.id), nullable=False)
    mc_date = Column(DateTime, default=date.today(), nullable=False)
    em = relationship('MedicalExaminationPatient', backref='medicalexaminationlist', lazy=True)


# Dang Ky Kham Benh
class MedicalRegister(BaseModel):
    __tablename__ = 'medicalregister'
    patient_id = Column(Integer, ForeignKey(PATIENT.id), nullable=False)
    register_date = Column(DateTime, nullable=False)

# Benh Nhan Kham Benh
class MedicalExaminationPatient(db.Model):
    __tablename__ = 'medicalexaminationpatient'
    mc_id = Column(Integer, ForeignKey(MedicalExaminationList.id), nullable=False, primary_key=True)
    patient_id = Column(Integer, ForeignKey(PATIENT.id), nullable=False, primary_key=True)


if __name__ == '__main__':
     db.create_all()



