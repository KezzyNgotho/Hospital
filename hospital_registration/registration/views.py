from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from .models import (
    Admin,
    Incharge,
    InpatientDetails,
    Patient,
    Attendance,
   PatientSignOut,
  
)
from .models import Attendance

def get_patient_details_by_type(request, is_inpatient):
    if request.method == "POST":
        student_number = request.POST.get("student_number")

        try:
            patient = Patient.objects.get(student_number=student_number)

            # Store the patient information in the session
            request.session["patient_number"] = patient.student_number
            request.session["patient_name"] = patient.full_name
            request.session["patient_gender"] = patient.gender

            if is_inpatient:
                return redirect("inpatient_signin", student_number=student_number)
            else:
                return redirect("outpatient_signin", student_number=student_number)

        except Patient.DoesNotExist:
            return redirect("patient_registration")

    return redirect("patient_attendance")



def patient_sign_out(request):
    if request.method == "POST":
        student_number = request.POST.get("student_number")
        activities = request.POST.get("activities")

        try:
            patient = Patient.objects.get(student_number=student_number)
            is_inpatient = patient.patient_type == Patient.INPATIENT

            patient_sign_out = PatientSignOut(
                check_in=timezone.now(),
                incharge=request.user,
                patient=patient,
                is_inpatient=is_inpatient,
            )
            patient_sign_out.save()

            request.session.pop("patient_number", None)
            request.session.pop("patient_name", None)
            request.session.pop("patient_gender", None)

            messages.success(request, "Sign out successful!")
            return redirect("patient_dashboard")

        except Patient.DoesNotExist:
            return redirect("patient_attendance")

    return redirect("patient_attendance")




def landing_page(request):
    return render(request, "registration/landing_page.html")


def admin_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            admin = Admin.objects.get(email=email, password=password)
            request.session["admin_id"] = admin.id
            return redirect("admin_dashboard")

        except Admin.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return render(request, "registration/admin_login.html")

    return render(request, "registration/admin_login.html")


def admin_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        admin = Admin(username=username, email=email, password=password)
        admin.save()

        return redirect("admin_login")

    return render(request, "registration/admin_signup.html")


def incharge_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        phone_number = request.POST["phone_number"]

        if Incharge.objects.filter(email=email).exists():
            messages.error(request, "An incharge with this email already exists.")
            return redirect("incharge_signup")

        incharge = Incharge(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number,
        )
        incharge.save()
        request.session["incharge_id"] = incharge.id
        return redirect("incharge_login")

    return render(request, "registration/incharge_signup.html")


def incharge_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            incharge = Incharge.objects.get(email=email, password=password)
            request.session["incharge_id"] = incharge.id
            return redirect("incharge_dashboard")

        except Incharge.DoesNotExist:
            messages.error(request, "Invalid credentials. Please try again.")
            response = render(request, "registration/incharge_login.html")
            request.session["incharge_not_found"] = True
            return response

    if request.session.get("incharge_not_found"):
        request.session.pop("incharge_not_found")
        return render(request, "registration/incharge_signup.html")

    return render(request, "registration/incharge_login.html")


def patient_registration(request):
    if request.method == "POST":
        student_number = request.POST.get("student_number")
        full_name = request.POST.get("full_name")
        gender = request.POST.get("gender")

        patient = Patient(student_number=student_number, full_name=full_name, gender=gender)
        patient.save()

        # Set the patient information in the session
        request.session["patient_number"] = patient.student_number
        request.session["patient_name"] = patient.full_name
        request.session["patient_gender"] = patient.gender

        messages.success(request, "Patient registered successfully.")
        return redirect("patient_attendance")

    return render(request, "registration/patient_registration.html")

def patient_attendance(request):
    if request.method == "POST":
        option = request.POST.get("option")
        student_number = request.POST.get("student_number")

        if option == "inpatient":
            request.session["is_inpatient"] = True
        elif option == "outpatient":
            request.session["is_inpatient"] = False

        # Store patient type and student number in the session
        request.session["patient_type"] = option
        request.session["student_number"] = student_number

        # Redirect to the appropriate sign-in view based on patient type
        if request.session["is_inpatient"]:
            return redirect("inpatient_signin", student_number=student_number)
        else:
            return redirect("outpatient_signin", student_number=student_number)

    return render(request, "registration/patient_attendance.html")


def inpatient_signin(request, student_number):
    patient = get_object_or_404(Patient, student_number=student_number)

    if request.method == "POST":
        incharge = get_object_or_404(Incharge, id=request.session.get("incharge_id"))
        room_number = request.POST.get("room_number")
        department = request.POST.get("department")

        # Retrieve patient type and student number from the session
        is_inpatient = request.session.get("is_inpatient", False)
        student_number = request.session.get("student_number")

        # Save the attendance with the correct patient type and student number
        attendance = Attendance(
            patient=patient,
            incharge=incharge,
            check_in=timezone.now(),
            room_number=room_number,
            department=department,
            patient_type=Attendance.INPATIENT if is_inpatient else Attendance.OUTPATIENT,
            student_number=student_number,
        )
        attendance.save()

        # Store patient information and patient type in the session
        request.session["patient_number"] = patient.student_number
        request.session["patient_name"] = patient.full_name
        request.session["patient_gender"] = patient.gender
        request.session["is_inpatient"] = is_inpatient

        return redirect("admin_dashboard")

    return render(
        request,
        "registration/inpatient_signin.html",
        {"patient": patient},
    )

def outpatient_signin(request, student_number):
    patient = get_object_or_404(Patient, student_number=student_number)

    if request.method == "POST":
        # Retrieve patient type and student number from the session
        is_inpatient = request.session.get("is_inpatient", False)
        student_number = request.session.get("student_number")

        # Get the incharge_id if available
        incharge_id = request.session.get("incharge_id")

        # Save the attendance with the correct patient type and student number
        attendance = Attendance(
            patient=patient,
            incharge_id=incharge_id,
            check_in=timezone.now(),
            patient_type=Attendance.INPATIENT if is_inpatient else Attendance.OUTPATIENT,
            student_number=student_number,
        )
        attendance.save()

        # Store patient information and patient type in the session
        request.session["patient_number"] = patient.student_number
        request.session["patient_name"] = patient.full_name
        request.session["patient_gender"] = patient.gender
        request.session["is_inpatient"] = is_inpatient

        return redirect("incharge_dashboard")

    return render(
        request,
        "registration/outpatient_signin.html",
        {"patient": patient},
    )
@transaction.atomic
def save_inpatient_details(request):
    if request.method == "POST":
        student_number = request.POST.get("student_number")
        room_number = request.POST.get("room_number")
        department = request.POST.get("department")

        try:
            patient = get_object_or_404(Patient, student_number=student_number)

            # Set the patient as an inpatient
            is_inpatient = True  # Since this is the inpatient_signin view, set is_inpatient to True
            # Store other patient details in the session
            request.session["patient_number"] = patient.student_number
            request.session["patient_name"] = patient.full_name
            request.session["patient_gender"] = patient.gender
            request.session["is_inpatient"] = is_inpatient
            request.session["room_number"] = room_number
            request.session["department"] = department

            if Incharge.objects.exists():
                incharge = Incharge.objects.first()
                attendance = Attendance(
                    patient=patient,
                    incharge=incharge,
                    check_in=timezone.now(),
                    room_number=room_number,
                    department=department,
                    patient_type=Patient.INPATIENT,  # Set the patient_type as "inpatient"
                    student_number=student_number,
                )
                attendance.save()
            else:
                # Handle the case when no Incharge object exists
                # Redirect to an appropriate page or display an error message
                pass

            return redirect("incharge_dashboard")

        except Patient.DoesNotExist:
            return redirect("patient_attendance")
    return redirect("patient_attendance")

   




def PatientSignup(request):
    if request.method == "POST":
        student_number = request.POST.get("student_number")
        activities = request.POST.get("activities")

        try:
            patient = Patient.objects.get(student_number=student_number)
            is_inpatient = patient.patient_type == 'inpatient'

            PatientSignOut = PatientSignOut(
                check_in=timezone.now(),
                incharge=request.user,
                patient=patient,
                is_inpatient=is_inpatient,
            )
            PatientSignOut.save()

            request.session.pop("patient_number", None)
            request.session.pop("patient_name", None)
            request.session.pop("patient_gender", None)

            messages.success(request, "Sign out successful!")
            return redirect("patient_dashboard")

        except Patient.DoesNotExist:
            return redirect("patient_attendance")

    return redirect("patient_attendance")


# ... Other views ...


def patient_dashboard(request):
    patient_number = request.session.get("patient_number")
    patient_name = request.session.get("patient_name")
    patient_gender = request.session.get("patient_gender")
    is_inpatient = request.session.get("is_inpatient", False)
    room_number = request.session.get("room_number")
    department = request.session.get("department")

    return render(
        request,
        "registration/patient_dashboard.html",
        {
            "patient_number": patient_number,
            "patient_name": patient_name,
            "patient_gender": patient_gender,
            "is_inpatient": is_inpatient,
            "room_number": room_number,
            "department": department,
        },
    )

def admin_dashboard(request):
    total_attendance = get_total_attendance()
    common_diseases_summary = get_common_diseases_summary()
    sign_out_patients = get_sign_out_patients()
    year = get_current_year()

    # Fetch inpatients and outpatients using the defined functions
    inpatients = get_inpatients()
    outpatients = get_outpatients()

    context = {
        "total_attendance": total_attendance,
        "inpatients": inpatients,
        "outpatients": outpatients,
        "common_diseases_summary": common_diseases_summary,
        "sign_out_patients": sign_out_patients,
        "year": year,
    }

    return render(request, "registration/admin_dashboard.html", context)

def get_inpatients():
    # Filter the Attendance model by patients with the patient_type as 'inpatient'
    inpatients = Attendance.objects.filter(patient_type=Attendance.INPATIENT)
    return inpatients

def get_outpatients():
    # Filter the Attendance model by patients with the patient_type as 'outpatient'
    outpatients = Attendance.objects.filter(patient_type=Attendance.OUTPATIENT)
    return outpatients


# ... Other views ...

def get_total_attendance():
    total_attendance = Attendance.objects.count()
    return total_attendance

def get_common_diseases_summary():
    common_diseases_summary = []
    # Implement your logic to populate common_diseases_summary here...
    return common_diseases_summary

def get_sign_out_patients():
    sign_out_patients = PatientSignOut.objects.all()
    return sign_out_patients

def get_current_year():
    import datetime
    return datetime.date.today().year

def incharge_dashboard(request):
    return render(request, "registration/incharge_dashboard.html")