from fastapi import FastAPI, HTTPException
import requests
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "VPBank API Service is running"}

@app.post("/get-noti")
def get_vpbank_notification(payload: dict):
    """
    API này nhận body (payload) từ bạn, chèn thêm headers của VPBank và gửi đi.
    """
    url = "https://asia-east2-vpbank-online-new---prod.cloudfunctions.net/get/notification"
    
    # Cấu hình các Header (Lưu ý: các key này có thể hết hạn, bạn nên truyền động nếu được)
    headers = {
        "Host": "asia-east2-vpbank-online-new---prod.cloudfunctions.net",
        "Accept": "application/json",
        "ChannelType": "NewEbank",
        "Accept-Language": "vi-VN,vi;q=0.9",
        "TokenKey": "RkZJSEFTSG5HUHdBNTI4SHZzc0FVdFhMZHlMUFlOcVcvMzZIYjhQd25xNndiUTloQnc9",
        "x-uiux-key": "37/8IiHnkkYelI2u8Lr/+Cidvj/UWlZZnc1hEDzQ1r/NcCqTXD+Ex81H9/E56g==",
        "User-Agent": "VPBankNEO/2026070402 CFNetwork/1410.1 Darwin/22.6.0",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "x-csrf-token": "5240998626390818506",
        "Cookie": "JSESSIONID=60EF683DA274A7CEA97B61912A9D960A.plf08.cluster01; Path=/cb; HttpOnly"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
