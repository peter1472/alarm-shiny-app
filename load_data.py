import argparse
from alarm_app.utils.db_loader import load_all_data

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='데이터 파일을 데이터베이스에 로드합니다.')
    parser.add_argument('--code', default='data/raw/code_master.txt', help='코드 마스터 파일 경로')
    parser.add_argument('--equipment', default='data/raw/equipment_mastert.xt', help='설비 마스터 파일 경로')
    parser.add_argument('--alarm', default='data/raw/alarm_master.txt', help='알람 마스터 파일 경로')
    parser.add_argument('--skip-code', action='store_true', help='코드 마스터 로드 건너뛰기')
    parser.add_argument('--skip-equipment', action='store_true', help='설비 마스터 로드 건너뛰기')
    parser.add_argument('--skip-alarm', action='store_true', help='알람 마스터 로드 건너뛰기')
    
    args = parser.parse_args()
    
    # 파일 경로 설정
    code_file = None if args.skip_code else args.code
    equipment_file = None if args.skip_equipment else args.equipment
    alarm_file = None if args.skip_alarm else args.alarm
    
    # 데이터 로드
    load_all_data(code_file, equipment_file, alarm_file)

if __name__ == "__main__":
    main() 