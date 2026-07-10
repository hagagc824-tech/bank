from fastapi import FastAPI
import requests
import json
import html
import ftfy  # Thư viện chuyên trị sửa lỗi font chữ ngoài hành tinh

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "VPBank API Service is running"}

@app.get("/get-noti")
def get_vpbank_notification():
    """
    API tự động bắt byte thô, ép giải mã và dùng AI-Fixer (ftfy) 
    để chuyển chữ loằng ngoằng thành tiếng Việt chuẩn.
    """
    url = "https://asia-east2-vpbank-online-new---prod.cloudfunctions.net/get/notification"
    
    headers = {
        "Host": "asia-east2-vpbank-online-new---prod.cloudfunctions.net",
        "Accept": "application/json",
        "ChannelType": "NewEbank",
        "Accept-Language": "vi-VN,vi;q=0.9",
        "TokenKey": "RkZJSEFTSDNraTQ4cmxwell2ejFZbGEyVDd1bDE2bU9jV3RVOTNCWE05SmdEZks3WWs9",
        "x-uiux-key": "37/8IiHnkkYelI2u8Lr/+Cidvj/UWlZZnc1hEDzQ1r/NcCqTXD+Ex81H9/E56g==",
        "User-Agent": "VPBankNEO/2026070402 CFNetwork/1410.1 Darwin/22.6.0",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "x-csrf-token": "5393083109632980188",
        "Cookie": "JSESSIONID=JSESSIONID=4B2C875B6EF5AC7ABEF8A9207F9E87DD.plf54.cluster04; Path=/cb; HttpOnly"
    }

    payload = {
        "page": 1,
        "pageSize": 20
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            # Đọc bằng byte thô (content) để tránh lỗi bộ giải mã mặc định của requests
            raw_bytes = response.content
            
            # Thử giải mã trực tiếp bằng utf-8
            decoded_text = raw_bytes.decode('utf-8', errors='ignore')
            
            # Dùng ftfy sửa triệt để lỗi chữ lộn xộn (Mojibake)
            fixed_text = ftfy.fix_text(decoded_text)
            
            # Chuyển chuỗi sạch thành JSON
            result = json.loads(fixed_text)
            
            # Làm sạch nốt các ký tự HTML (&ocirc;, &amp;,...) nếu còn sót lại
            if "data" in result and "notification" in result["data"]:
                for noti in result["data"]["notification"]:
                    if "title" in noti and noti["title"]:
                        noti["title"] = html.unescape(ftfy.fix_text(noti["title"]))
                    if "content" in noti and noti["content"]:
                        noti["content"] = html.unescape(ftfy.fix_text(noti["content"]))
            
            return result
        else:
            return {
                "error": f"VPBank trả về mã lỗi {response.status_code}",
                "detail": response.text
            }
            
    except Exception as e:
        return {"error": "Lỗi xử lý hệ thống mã hóa", "message": str(e)}
