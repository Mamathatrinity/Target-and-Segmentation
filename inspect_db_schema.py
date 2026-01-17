"""
Inspect actual database table structure
Shows what columns actually exist in segments table
"""
import pymysql
import pymysql.cursors

try:
    connection = pymysql.connect(
        host='mysql-customerengagement-dev.mysql.database.azure.com',
        port=3306,
        user='hcp_targetandsegment_user',
        password='yyug23@ER12fddT',
        database='mysql_hcp_targetandsegmentation_dev',
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=30
    )
    
    cursor = connection.cursor()
    
    # Get table structure
    cursor.execute("DESCRIBE segments")
    columns = cursor.fetchall()
    
    print("\n" + "="*80)
    print("SEGMENTS TABLE STRUCTURE")
    print("="*80 + "\n")
    
    print(f"{'Field':<25} {'Type':<30} {'Null':<8} {'Key':<8} {'Default':<15}")
    print("-"*90)
    
    for col in columns:
        field = col.get('Field', '')
        type_ = col.get('Type', '')
        null = col.get('Null', '')
        key = col.get('Key', '')
        default = str(col.get('Default', ''))[:15]
        
        print(f"{field:<25} {type_:<30} {null:<8} {key:<8} {default:<15}")
    
    print("\n" + "="*80)
    print("SAMPLE QUERY RESULTS")
    print("="*80 + "\n")
    
    # Get a few segments to see structure
    cursor.execute("SELECT * FROM segments LIMIT 3")
    results = cursor.fetchall()
    
    print(f"Total columns: {len(columns)}")
    print(f"Sample rows: {len(results)}")
    
    if results:
        print("\nSample data:")
        for i, row in enumerate(results):
            print(f"\nRow {i+1}:")
            for key, value in row.items():
                print(f"  {key}: {value}")
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
