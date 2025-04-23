from dataclasses import dataclass
from typing import Optional

@dataclass
class CodeMaster:
    type: str
    code: str
    value: str
    category: str
    eng_category: str
    code_id: Optional[int] = None
    
@dataclass
class EquipmentMaster:
    machinename: str
    process_c: str
    room_c: str
    equipment_c: str
    eq_group_c: str
    eq_class_c: str
    logistics_c: str
    floor_c: str
    polarity_c: str
    eq_detail: str
    mcs_source: str
    mcs_name: str
    is_virtual: bool
    is_excluded: bool
    upper_cim: str
    alarm_group: str
    supplier: str
    remarks: str
    eq_id: Optional[int] = None

@dataclass
class AlarmMaster:
    alarmid: int
    alarmcode: int
    category: str
    description: str
    severity: int
    alarm_cause: str
    severity_desc: str
    severity_ratio: float
    alarm_id: Optional[int] = None

@dataclass
class CodedAttribute:
    column_name: str
    is_coded: bool
    code_category: str
    code_source: str
    attr_id: Optional[int] = None 