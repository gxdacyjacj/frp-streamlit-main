"""
数据库迁移脚本：从Excel文件迁移到Railway MySQL
使用方法：
1. 确保database 4.xlsx文件在当前目录
2. Railway数据库连接信息已配置
3. 运行此脚本进行数据迁移
"""

import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import os
from dotenv import load_dotenv
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# Excel文件路径
EXCEL_FILE_PATH = './database 4.xlsx'

# Railway数据库配置（使用Railway环境变量）
RAILWAY_DB_CONFIG = {
    'host': 'switchback.proxy.rlwy.net',  # 使用外部可访问的主机名
    'port': 17121,                        # 外部端口
    'user': 'root',
    'password': 'zAFTUZnwLefvYBrVaQSZNndcSmnZeuRe',
    'database': 'railway'
}

def export_from_excel():
    """从Excel文件导出数据"""
    print("🔄 正在从Excel文件读取数据...")
    
    try:
        # 检查Excel文件是否存在
        if not os.path.exists(EXCEL_FILE_PATH):
            print(f"❌ Excel文件不存在: {EXCEL_FILE_PATH}")
            print("请确保database 4.xlsx文件在当前目录")
            return None
        
        # 读取Excel文件
        print("📖 正在读取Excel文件...")
        df = pd.read_excel(EXCEL_FILE_PATH, header=3, engine='openpyxl')
        print(f"✅ 成功读取Excel文件，数据形状: {df.shape}")
        
        # 取前134列（适配database 4.xlsx的新结构）
        df = df.iloc[:, :134]
        print(f"使用前134列，调整后形状: {df.shape}")
        
        # 清理数据
        print("🧹 正在清理数据...")
        special_values = ['SMD', 'Notreported', 'N/A', '', ' ', 'nan', 'NULL', 'None']
        df = df.replace(special_values, None)
        df = df.replace({np.nan: None})
        
        # 处理数值字段
        numeric_positions = [5, 18, 34, 35]  # Year, diameter, Value1_1, COV1_1等
        for pos in numeric_positions:
            if pos < len(df.columns):
                df.iloc[:, pos] = pd.to_numeric(df.iloc[:, pos], errors='coerce')
        
        # 限制文本长度，防止数据库字段溢出
        for col_idx in range(len(df.columns)):
            if df.iloc[:, col_idx].dtype == 'object':
                df.iloc[:, col_idx] = df.iloc[:, col_idx].astype(str).str[:2000]
                df.iloc[:, col_idx] = df.iloc[:, col_idx].replace('None', None)
        
        print(f"✅ 数据清理完成，共 {len(df)} 条记录")
        
        # 保存到CSV文件作为备份
        df.to_csv('frp_data_export.csv', index=False)
        print("✅ 数据已保存到 frp_data_export.csv")
        
        return df
    
    except Exception as e:
        print(f"❌ Excel读取失败: {e}")
        return None

def import_to_railway(df):
    """导入数据到Railway数据库"""
    if df is None:
        print("❌ 没有数据需要导入")
        return False
        
    print("🔄 正在导入数据到Railway...")
    
    try:
        # 连接Railway数据库
        railway_engine = create_engine(
            f"mysql+pymysql://{RAILWAY_DB_CONFIG['user']}:{RAILWAY_DB_CONFIG['password']}@{RAILWAY_DB_CONFIG['host']}:{RAILWAY_DB_CONFIG['port']}/{RAILWAY_DB_CONFIG['database']}"
        )
        
        # 定义列名映射（与database 4.xlsx结构对应）
        column_names = [
            'feature_name', 'Title', 'Author', 'SCI', 'Journal_or_Conference_name',
            'Year', 'No_field', 'no_field_secondary', 'Fiber_type', 'Fiber_type_detail',
            'Matrix_type', 'Matrix_type_detail', 'glass_transition_temperature', 
            'glass_transition_temperature_run_2', 'cure_ratio', 'Fiber_content_weight',
            'Fiber_content_volume', 'Void_content', 'diameter', 'average_area',
            'nominal_area', 'rib', 'surface_treatment', 'Water_absorption_at_saturation',
            'Water_absorption_test_standard', 'Water_absorption_note', 'Brand_name',
            'Manufacturer', 'Important_notes', 'Notes_of_rebar', 'Target_parameter',
            'note_of_target_parameter', 'num_1', 'note_of_number', 'Value1_1',
            'COV1_1', 'note_of_Value1', 'Value2_1', 'COV2_1', 'Value2note_1',
            'Value3_1', 'COV3_1', 'Value3note_1', 'SEM_T_BCBT', 'SEM_L_BCBT',
            'OTHER_main', 'OTHER1_1', 'FTIR_1', 'note_1', 'temperature',
            'note_of_temperature', 'time_field', 'note_of_time', 'concrete',
            'pH_of_concrete', 'strength_of_concrete', 'crack', 'cover',
            'note_of_concrete', 'pH_1', 'pHafter', 'ingredient_1', 'pH_2',
            'RH_1', 'ingredient_2', 'note_2', 'Location', 'Effektive_Klimaklassifikation',
            'field_average_humidity', 'field_average_temperature', 'pH_2_additional',
            'Ingrediant_additional', 'number_field', 'type_field', 'SolutionorMoisture',
            'cycle_pH', 'cycle_pH_after', 'cycle_ingredient', 'temp', 'temp2',
            'RH_2', 'RH2', 'OTHER1_2', 'OTHER2_main', 'time_in_cycle', 'note_3',
            'UV', 'note_4', 'stress_or_strain', 'type_of_load', 'value_load',
            'ultimate_tensile_strength', 'tensile_modulus', 'note_5', 'after_condition',
            'note_6', 'num_2', 'Value1_2', 'COV1_2', 'Value1note', 'retention1',
            'Value2_2', 'COV2_2', 'Value2note_2', 'retention2', 'Value3_2',
            'COV3_2', 'Value3note_2', 'retention3', 'num_3', 'water_absorption_ratio',
            'COV_1', 'note_7', 'num_4', 'glass_transition_temperature_2', 'run2',
            'COV_2', 'cure_ratio_2', 'note_8', 'num_5', 'OTHERS', 'OTHERS_note',
            'SEM_T_BCAT', 'SEM_L_BCAT', 'SEM_T_ACBT', 'SEM_L_ACBT', 'SEM_T_ACAT',
            'SEM_L_ACAT', 'other_lower', 'other2_final', 'note_9', 'FTIR_2',
            'note_10', 'important_note'
        ]
        
        # 确保DataFrame有正确的列名
        df.columns = column_names[:len(df.columns)]
        
        # 导入数据到research_data表
        df.to_sql('research_data', railway_engine, if_exists='replace', index=False, method='multi')
        print(f"✅ 成功导入 {len(df)} 条记录到Railway数据库 (research_data表)")
        
        return True
        
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        print("请检查Railway数据库连接信息是否正确")
        return False

def main():
    print("🚂 开始数据库迁移到Railway")
    print("=" * 50)
    
    # 第一步：从Excel文件导出
    df = export_from_excel()
    
    if df is not None:
        print(f"\n数据概况:")
        print(f"- 总行数: {len(df)}")
        print(f"- 总列数: {len(df.columns)}")
        print(f"- 数据大小: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        
        # 第二步：导入到Railway
        if import_to_railway(df):
            print("\n🎉 数据迁移完成！")
            print("现在可以更新应用配置使用Railway数据库")
            print("数据已从database 4.xlsx成功导入到Railway MySQL")
        else:
            print("\n❌ 数据迁移失败")
    
    print("=" * 50)

if __name__ == "__main__":
    main()