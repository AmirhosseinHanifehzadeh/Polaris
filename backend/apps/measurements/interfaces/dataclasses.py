from libs import dataclasses
from typing import List, Optional
from datetime import datetime


class MeasurementDTO(dataclasses.BaseModel):
    id: int
    timestamp: datetime
    latitude: float
    longitude: float
    technology: str
    plmn_id: Optional[str] = None
    lac: Optional[int] = None
    rac: Optional[int] = None
    tac: Optional[int] = None
    cell_id: Optional[int] = None
    frequency_band: Optional[str] = None
    arfcn: Optional[int] = None
    rsrp: Optional[float] = None
    rsrq: Optional[float] = None
    rscp: Optional[float] = None
    ec_no: Optional[float] = None
    rxlev: Optional[float] = None
    download_rate: Optional[float] = None
    upload_rate: Optional[float] = None
    ping_response_time: Optional[float] = None
    dns_response_time: Optional[float] = None
    web_response_time: Optional[float] = None
    sms_delivery_time: Optional[float] = None
    created_at: datetime
    updated_at: datetime


class CreateMeasurementReq(dataclasses.BaseModel):
    timestamp: datetime
    latitude: float
    longitude: float
    technology: str
    plmn_id: Optional[str] = None
    lac: Optional[int] = None
    rac: Optional[int] = None
    tac: Optional[int] = None
    cell_id: Optional[int] = None
    frequency_band: Optional[str] = None
    arfcn: Optional[int] = None
    rsrp: Optional[float] = None
    rsrq: Optional[float] = None
    rscp: Optional[float] = None
    ec_no: Optional[float] = None
    rxlev: Optional[float] = None
    download_rate: Optional[float] = None
    upload_rate: Optional[float] = None
    ping_response_time: Optional[float] = None
    dns_response_time: Optional[float] = None
    web_response_time: Optional[float] = None
    sms_delivery_time: Optional[float] = None


class MeasurementListReq(dataclasses.BaseModel):
    technology: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: Optional[int] = 100
    offset: Optional[int] = 0


class MeasurementListResponse(dataclasses.BaseModel):
    count: int
    results: List[MeasurementDTO]


class BulkCreateMeasurementReq(dataclasses.BaseModel):
    measurements: List[CreateMeasurementReq]


class BulkCreateMeasurementResponse(dataclasses.BaseModel):
    created_count: int
    results: List[MeasurementDTO] 