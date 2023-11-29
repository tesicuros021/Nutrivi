from django.shortcuts import redirect, render, get_object_or_404
from .models import Patients, Meetings  # make sure to import your models
from django.db.models import Q

def unos(request):
    if request.method == 'POST':
            ime = request.POST.get('ime')
            prezime = request.POST.get('prezime')
            datum_rodjenja = request.POST.get('datum_rodjenja')
            pol = request.POST.get('pol')
            kontakt_telefon = request.POST.get('kontakt_telefon')
            email = request.POST.get('email')
            adresa = request.POST.get('adresa')
            Patients.objects.create(
                ime=ime,
                prezime=prezime,
                datum_rodjenja=datum_rodjenja,
                pol=pol,
                kontakt_telefon=kontakt_telefon,
                email=email,
                adresa=adresa
            )
            return redirect('/ponuda')
    return render(request, 'unos.html')

def ponuda(request):
    query = request.GET.get('query', '')
    patients = Patients.objects.filter(Q(ime__icontains=query) | Q(prezime__icontains=query))
    context = {
        'patients': patients
    }
    return render(request, 'ponuda.html', context)

def detalji(request, patient_id):
    patient = get_object_or_404(Patients, patient_id=patient_id)

    # Query to get all meetings for this specific patient
    meetings = Meetings.objects.filter(patient=patient)

    # Extracting patient_meeting_id values from meetings
    patient_meeting_ids = [meeting.patient_meeting_id for meeting in meetings]

    context = {
        'patient': patient,
        'patient_meeting_ids': patient_meeting_ids,
    }
    return render(request, 'detalji.html', context)

def novisastanak(request, patient_id):
    if request.method == 'POST':
        # Create a new Meetings instance
        patient = get_object_or_404(Patients, patient_id=patient_id)
        meeting = Meetings(
            patient=patient,
            datum_sastanka=request.POST.get('datum_sastanka'),
            dijagnoza_za_ishranu=request.POST.get('dijagnoza_za_ishranu', ''),
            preporuka_za_ishranu=request.POST.get('preporuka_za_ishranu', ''),
            bmi=float(request.POST.get('bmi', 0)),
            telesna_masa=float(request.POST.get('telesna_masa', 0)),
            visina=float(request.POST.get('visina', 0)),
            procenat_spoljasnje_masti=float(request.POST.get('procenat_spoljasnje_masti', 0)),
            procenat_unutrasnje_masti=float(request.POST.get('procenat_unutrasnje_masti', 0)),
            procenat_misica=float(request.POST.get('procenat_misica', 0)),
            procenat_vode=float(request.POST.get('procenat_vode', 0)),
        )
        meeting.save()  # Save the meeting instance, and meeting_id will be generated automatically

        return redirect('/detalji/' + str(patient_id))
    return render(request, 'novisastanak.html', {'patient_id': patient_id})

def sastanak(request, patient_id, patient_meeting_id):
    patient = get_object_or_404(Patients, patient_id=patient_id)
    meeting = get_object_or_404(Meetings, patient=patient, patient_meeting_id=patient_meeting_id)
    context = {'meeting': meeting, 'patient': patient}
    return render(request, 'sastanak.html', context)

def brisanje(request, x):
    Patients.objects.get(patient_id=x).delete()
    return redirect('/ponuda')

def nutrivita(request):
    return render(request, 'nutrivita.html')