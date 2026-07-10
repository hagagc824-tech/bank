from fastapi import FastAPI
import requests
import html

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "VPBank API Service is running"}

@app.get("/get-noti")
def get_vpbank_notification():
    """
    API tự động sửa lỗi font mã hóa (Encoding) từ VPBank,
    trả về dữ liệu tiếng Việt chuẩn 100% hiển thị mượt mà trên trình duyệt.
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
            # BƯỚC QUAN TRỌNG: Ép sửa lỗi font mã hóa lỗi từ nguồn VPBank sang UTF-8 tiếng Việt
            corrected_text = response.content.decode('utf-8', errors='ignore')
            result = json_data = response.json()
            
            # Nếu ép JSON gốc vẫn lỗi chữ, ta nạp lại từ chuỗi đã sửa encoding
            try:
                import json
                result = json.loads(corrected_text)
            except:
                pass

            # Tiếp tục làm sạch các ký tự HTML cũ
            if "data" in result and "notification" in result["data"]:
                for noti in result["data"]["notification"]:
                    if "title" in noti and noti["title"]:
                        # Sửa lỗi font kép (nếu có) và dịch ký tự HTML
                        try:
                            noti["title"] = noti["title"].encode('latin1').decode('utf-8')
                        except:
                            pass
                        noti["title"] = html.unescape(noti["title"])
                        
                    if "content" in noti and noti["content"]:
                        try:
                            noti["content"] = noti["content"].encode('latin1').decode('utf-8')
                        except:
                            pass
                        noti["content"] = html.unescape(noti["content"])
            
            return result
        else:
            return {
                "error": f"VPBank trả về mã lỗi {response.status_code}",
                "detail": response.text
            }
            
    except Exception as e:
        return {"error": "Lỗi hệ thống khi xử lý dữ liệu", "message": str(e)}
