from langchain_core.tools import tool

FLIGHTS_DB: dict[tuple[str, str], list[dict]] = {
    ("Hà Nội", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "07:20",
            "price": 1_450_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "14:00",
            "arrival": "15:20",
            "price": 2_800_000,
            "class": "business",
        },
        {
            "airline": "VietJet Air",
            "departure": "08:30",
            "arrival": "09:50",
            "price": 890_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "11:00",
            "arrival": "12:20",
            "price": 1_200_000,
            "class": "economy",
        },
    ],
    ("Hà Nội", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "07:00",
            "arrival": "09:15",
            "price": 2_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "10:00",
            "arrival": "12:15",
            "price": 1_350_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "16:00",
            "arrival": "18:15",
            "price": 1_100_000,
            "class": "economy",
        },
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "08:10",
            "price": 1_600_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "07:30",
            "arrival": "09:40",
            "price": 950_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "12:00",
            "arrival": "14:10",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "18:00",
            "arrival": "20:10",
            "price": 3_200_000,
            "class": "business",
        },
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "09:00",
            "arrival": "10:20",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "13:00",
            "arrival": "14:20",
            "price": 780_000,
            "class": "economy",
        },
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "08:00",
            "arrival": "09:00",
            "price": 1_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "15:00",
            "arrival": "16:00",
            "price": 650_000,
            "class": "economy",
        },
    ],
}

HOTELS_DB: dict[str, list[dict]] = {
    "Đà Nẵng": [
        {
            "name": "Mường Thanh Luxury",
            "stars": 5,
            "price_per_night": 1_800_000,
            "area": "Mỹ Khê",
            "rating": 4.5,
        },
        {
            "name": "Sala Danang Beach",
            "stars": 4,
            "price_per_night": 1_200_000,
            "area": "Mỹ Khê",
            "rating": 4.3,
        },
        {
            "name": "Fivitel Danang",
            "stars": 3,
            "price_per_night": 650_000,
            "area": "Sơn Trà",
            "rating": 4.1,
        },
        {
            "name": "Memory Hostel",
            "stars": 2,
            "price_per_night": 250_000,
            "area": "Hải Châu",
            "rating": 4.6,
        },
        {
            "name": "Christina's Homestay",
            "stars": 2,
            "price_per_night": 350_000,
            "area": "An Thượng",
            "rating": 4.7,
        },
    ],
    "Phú Quốc": [
        {
            "name": "Vinpearl Resort",
            "stars": 5,
            "price_per_night": 3_500_000,
            "area": "Bãi Dài",
            "rating": 4.4,
        },
        {
            "name": "Sol by Meliá",
            "stars": 4,
            "price_per_night": 1_500_000,
            "area": "Bãi Trường",
            "rating": 4.2,
        },
        {
            "name": "Lahana Resort",
            "stars": 3,
            "price_per_night": 800_000,
            "area": "Dương Đông",
            "rating": 4.0,
        },
        {
            "name": "9Station Hostel",
            "stars": 2,
            "price_per_night": 200_000,
            "area": "Dương Đông",
            "rating": 4.5,
        },
    ],
    "Hồ Chí Minh": [
        {
            "name": "Rex Hotel",
            "stars": 5,
            "price_per_night": 2_800_000,
            "area": "Quận 1",
            "rating": 4.3,
        },
        {
            "name": "Liberty Central",
            "stars": 4,
            "price_per_night": 1_400_000,
            "area": "Quận 1",
            "rating": 4.1,
        },
        {
            "name": "Cochin Zen Hotel",
            "stars": 3,
            "price_per_night": 550_000,
            "area": "Quận 3",
            "rating": 4.4,
        },
        {
            "name": "The Common Room",
            "stars": 2,
            "price_per_night": 180_000,
            "area": "Quận 1",
            "rating": 4.6,
        },
    ],
}


def format_currency(price) -> str:
    # 1. Convert to int first (handles both "650000" and 650000)
    # 2. Use : , to add thousands separators
    # 3. Replace , with . for Vietnamese format
    try:
        numeric_price = int(price)
        formatted_number = f"{numeric_price:,}".replace(",", ".")
        return f"({formatted_number}đ)"
    except (ValueError, TypeError):
        # Fallback if the input isn't a valid number
        return f"({price}đ)"


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
        origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
        destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc') Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến."""

    def format_flights(flights: list[dict], origin: str, destination: str) -> str:
        result = f"Các chuyến bay từ {origin} đến {destination}:\n"
        for f in flights:
            result += f"- {f['airline']} ({f['class']}): {f['departure']} -> {f['arrival']} | Giá: {format_currency(f['price'])}\n"

        return result.strip()

    # --------------------------------

    flights = FLIGHTS_DB.get((origin, destination))
    if flights:
        return format_flights(flights, origin, destination)
    else:
        other_flights = FLIGHTS_DB.get((destination, origin))
        if other_flights:
            return format_flights(other_flights, destination, origin)
        else:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."


# TODO: Sinh viên tự triển khai
# - Tra cứu FLIGHTS_DB với key (origin, destination)
# - Nếu tìm thấy → format danh sách chuyến bay dễ đọc, bao gồm giá tiền
# - Nếu không tìm thấy → thử tra ngược (destination, origin) xem có không,
# - nếu cũng không có → "Không tìm thấy chuyến bay từ {origin} đến {destination}." # - Gợi ý: format giá tiền có dấu chấm phân cách (1.450.000đ) pass


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi
    đêm.
    Tham số:
        city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
        max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới
        hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực,
    rating.
    """
    hotels = HOTELS_DB.get(city, [])
    filtered_hotels = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
    sorted_hotels = sorted(filtered_hotels, key=lambda h: h["rating"], reverse=True)

    if not sorted_hotels:
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {max_price_per_night}/đêm. Hãy thử tăng ngân sách."

    result = f"Khách sạn phù hợp tại {city}:\n"
    for h in sorted_hotels:
        result += f"- {h['name']} ({h['stars']} sao): {format_currency(h['price_per_night'])} / đêm\n"

    return result.strip()


# TODO: Sinh viên tự triển khai # - Tra cứu HOTELS_DB[city]
# - Lọc theo max_price_per_night # - Sắp xếp theo rating giảm dần
# - Format đẹp. Nếu không có kết quả → "Không tìm thấy khách sạn tại {city} với giá dưới {max_price_per_night}/đêm. Hãy thử tăng ngân sách." pass


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí. Tham số:
        total_budget: tổng ngân sách ban đầu (VNĐ)
        expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
    định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi phí các khoản chi và số tiền còn lại. Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu."""

    # parse expenses string to dict
    expenses_dict = dict(item.split(":") for item in expenses.split(","))

    # calculate total expenses
    total_expenses = sum(int(price) for price in expenses_dict.values())

    # calculate remaining balance
    remaining_balance = total_budget - total_expenses

    # format expense table
    expense_table = "\n".join(
        [
            f"- {name}: {format_currency(str(price))}"
            for name, price in expenses_dict.items()
        ]
    )

    # return result
    if remaining_balance < 0:
        return f"Vượt ngân sách {format_currency(str(-remaining_balance))}! Cần điều chỉnh."
    else:
        return f"Bảng chi phí:\n{expense_table}\nTổng chi: {format_currency(str(total_expenses))}\nNgân sách: {format_currency(str(total_budget))}\nCòn lại: {format_currency(str(remaining_balance))}"


# TODO: Sinh viên tự triển khai
# - Parse chuỗi expenses thành dict {tên: số_tiền} # - Tính tổng chi phí
# - Tính số tiền còn lại = total_budget - tổng chi phí # - Format bảng chi phí:
# Bảng chi phí:
# - Vé máy bay: 890.000đ   #	- Khách sạn: 650.000đ #	---
# Tổng chi: 1.540.000đ #	Ngân sách: 5.000.000đ #	Còn lại: 3.460.000đ
# - Nếu âm → "Vượt ngân sách X đồng! Cần điều chỉnh."
# - Xử lý lỗi: nếu expenses format sai → trả về thông báo lỗi rõ ràng pass
