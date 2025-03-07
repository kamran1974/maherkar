from kavenegar import *
def send_sms(phone,code,template):
    try:
        api = KavenegarAPI('65553661307051326F6B50306B656B6E5046362F71356647716C5A6357645062545374685545777137484D3D')
        params = {
            'receptor': phone,
            'template': template,
            'token': code,
            'type': 'sms',#sms vs call
            }   
        response = api.verify_lookup(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)
        
