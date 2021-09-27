from api_mobile.utils import get_working_policy
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from api_mobile import osago_android_api

app = FastAPI(title="Osago Policy API")


async def check_working_policy():
    policy_info = get_working_policy()
    if len(policy_info < 1):
        return

    serial, policy = policy_info

    try:
        data = await osago_android_api(serial, policy)
    except ValueError:
        return
    else:
        errors = data.get("errors", [])
        if (len(errors) > 0 and errors[0]["code"] == 617) or not data.get("policyInfoExtended", []):
            return False
        else:
            return True


@app.get("/api")
async def api_page(serial: str, policy: str):
    # -- Calling osago check
    try:
        data = await osago_android_api(serial, policy)
    except ValueError:
        return JSONResponse({
            "status": "error", "message": "Неверный серийный номер"
        }, status.HTTP_422_UNPROCESSABLE_ENTITY)

    # -- Checking response

    if not data:  # If request error
        return JSONResponse({
            "status": "error", "message": "Сервис autoins.ru не доступен, повторите попытку позже",
        }, status.HTTP_503_SERVICE_UNAVAILABLE)

    errors = data.get("errors", [])
    if (len(errors) > 0 and errors[0]["code"] == 617) or not data.get("policyInfoExtended", []):
        ##
        is_correct = await check_working_policy()
        if is_correct:
            return JSONResponse({
                "status": "error", "message": "Договор не найден"
            }, status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return JSONResponse({
                "status": "error", "message": "Неверный ответ от сервера"
            }, status.HTTP_429_TOO_MANY_REQUESTS)

    # -- Return parsed data
    info = data["policyInfoExtended"][0]

    periods = []

    for i in range(1, 3+1):
        period_beg = info.get(f"period{i}Beg")
        period_end = info.get(f"period{i}End")

        if period_beg and period_end:
            periods.append([period_beg, period_end])

    result = {
        "status": "ok",
        "seria": info.get("policySerialKey"),
        "nomer": info.get("policyNumberKey"),
        "sk": info.get("insurerName"),
        "createData": info.get("dateCreate"),
        "startDate": info.get("dateActionBeg"),
        "endDate": info.get("dateActionEnd"),
        "regnum": info.get("licensePlate"),
        "vin": info.get("vin"),
        "vinBody": info.get("bodyNumber"),
        "vinChassis": info.get("chassisNumber"),
        "brand": info.get("markCar"),
        "model": info.get("modelCar"),
        "periods": periods,
        # "policyNumber": info.get("policyId"),
        # "policyStateSecret": info.get("policyStateSecret"),
        "policyStatus": "active" if info.get("policyState") == "ACTIVE" else "inactive",
    }

    return result
