import athenahealthapi
import datetime

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

def get_open_appts(dates):
#def get_open_appts():

    dateformat = '%m/%d/%Y'

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
            provider_t = extract_time(a['starttime'])
            patient_t = (d['start_time']['hour']*60 + d['start_time']['minute'])
            provider_delta = int(a['duration'])
            patient_delta = 10
            if ((provider_t <= patient_t) and
            ((patient_t + patient_delta) <= (provider_t + provider_delta))):
                print "yes"
                open_appts.append({'date': a['date'], 'time': a['starttime']})

            #if int(a['starttime'].split(':')[0]) <= d['start']['hour']:


        #print "OPEN APPTS"
        #print open_appts


    #d1_start = datetime.datetime(2016, 4, 24)
    #d1_end = datetime.datetime(2016, 4, 30)

    #open_appts = api.GET('/appointments/open', {
        #'departmentid': 1,
        #'startdate': d1_start.strftime(dateformat),
        #'enddate': d1_end.strftime(dateformat),
        #'limit': 3,
        #'appointmenttypeid': 82,
        #'providerid': 71
    #})

    ## change the keys in appt to make it usable in scheduling
    #appt = open_appts['appointments'][0]
    #print 'Open appointment:'
    #print appt
    ##appt['appointmenttime'] = appt.pop('starttime')
    ##appt['appointmentdate'] = appt.pop('date')
    #print appt.pop('starttime')
    #print appt.pop('date')
    #print appt.pop('duration')

    #return open_appts['appointments']
    return open_appts