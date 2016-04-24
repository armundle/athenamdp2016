import athenahealthapi
import datetime
import calendar

# Setup
key = '28px28k6z5t5cr9mjj6rr54b'  # clientID
secret = 'cJhszqRQ8SAAEB4'  # clientSecret
version = 'preview1'
practiceid = 195900


api = athenahealthapi.APIConnection(version,
                                    key,
                                    secret,
                                    practiceid)


def path_join(*parts):
    return ''.join('/' + str(part).strip('/') for part in parts if part)


def extract_time(time):
    h = int(time.split(':')[0])
    m = int(time.split(':')[1])
    return (h*60+m)


def format_12(time):
    h = int(time.split(':')[0])
    m = int(time.split(':')[1])
    if h > 12:
        h = 24 - h
        suffix = "PM"
    else:
        suffix = "AM"

    return (str(h) + ":" + str(m).zfill(2) + " " + suffix)


def get_datetime(date):
    d = date.split('/')
    date_unfmt = datetime.datetime(int(d[2]),
                                    int(d[0]),
                                    int(d[1]))
    return date_unfmt


def format_date(fmt, d_datetime):
    return d_datetime.strftime(fmt)


def get_open_appts(dates):

    dateformat = '%m/%d/%Y'
    response_dateformat = '%Y-%m-%d'

    open_appts =[]
    for d in dates:
        start = datetime.datetime(d['start_time']['year'],
                                  d['start_time']['month'],
                                  d['start_time']['day'])
        appt_day = api.GET('/appointments/open', {
            'departmentid': 1,
            'startdate': start.strftime(dateformat),
            'enddate': start.strftime(dateformat),
            'limit': 10,
            'appointmenttypeid': 82,
            'providerid': 71
        })

        for a in appt_day['appointments']:
            #print a
            provider_t = extract_time(a['starttime'])
            patient_t = (d['start_time']['hour']*60 + d['start_time']['minute'])
            provider_delta = int(a['duration'])
            patient_delta = 10
            if ((provider_t <= patient_t) and
            ((patient_t + patient_delta) <= (provider_t + provider_delta))):
                date = a['date'].split('/')
                date_unfmt = datetime.datetime(int(date[2]),
                                               int(date[0]),
                                               int(date[1]))
                return_date = date_unfmt.strftime(response_dateformat)
                day = calendar.day_name[date_unfmt.weekday()]
                time = a['starttime']
                return_time = format_12(time)
                open_appts.append({'date': (str(return_date) + " " + return_time),
                                  'day': day,
                                  '_appointment_id': a['appointmentid']})
    return open_appts


def book_appointment(appointment):

    appointment_id = appointment['_appointment_id']
    #print appointment_id
    appointment_info = {
        'appointmenttypeid': 82,
        'departmentid': 1,
        'patientid': 22607
    }

    book = api.PUT(path_join('/appointments',
                               appointment_id), appointment_info)
    #print 'Response to booking appointment:'
    #print book
    return book



def get_booked_appointment():

    patientid = 22607

    booked = api.GET(path_join('/patients', patientid,
                               '/appointments'))

    return booked


def reset_appointment():
    appointments = get_booked_appointment()['appointments']
    #appointmentids = []
    patientid = 22607
    response = []
    for a in appointments:
        appointmentid = a['appointmentid']
        appointment_info = {
            'appointmentid': appointmentid,
            'patientid': 22607,
            'cancellationreason': "hello"
        }

        response.append(api.PUT(path_join('/appointments', appointmentid,
                                '/cancel'), appointment_info))

    return response
