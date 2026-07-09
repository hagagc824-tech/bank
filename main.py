from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "VPBank API Service is running"}

@app.get("/get-noti")
def get_vpbank_notification():
    """
    API cấu hình dạng GET để có thể bấm xem trực tiếp từ trình duyệt điện thoại.
    Nó sẽ tự động gửi gói tin POST cùng các Header cần thiết sang hệ thống VPBank.
    """
    url = "https://asia-east2-vpbank-online-new---prod.cloudfunctions.net/get/notification"
    
    # Các thông tin định danh bạn lấy từ App
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

    # Gói tin nhắn (Payload) mặc định của chức năng lấy thông báo
    payload = {
        "page": 1,
        "pageSize": 20
    }

    try:
        # Hệ thống của bạn nhận GET nhưng sẽ tạo request POST sang VPBank
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            # Nếu lỗi (ví dụ Token hết hạn), trả về chi tiết lỗi từ VPBank
            return {
                "error": f"VPBank returned status code {response.status_code}",
                "detail": response.text
            }
            
    except Exception as e:
        return {"error": "Lỗi kết nối đến server VPBank", "message": str(e)}
