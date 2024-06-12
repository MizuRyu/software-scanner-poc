from PIL import Image
import os
import datetime

input_path = os.path.join(os.getcwd(), 'pngs')
output_dir = os.path.join(os.getcwd(), 'imgs')

# 出力ディレクトリが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 指定ディレクトリのファイルを取得
files = os.listdir(input_path)
print(f"files: {files}")

# 取得したファイルからPNGファイルのみ取得
pngs = [f for f in files if f.lower().endswith('.png')]

# 出力ファイル名用に現在時刻の取得
dt_now = datetime.datetime.now().strftime('%y%m%d_%H%M%S')

# pngをjpgに変換する
for p in pngs:
    input_img_path = os.path.join(input_path, p)
    output_img_name = os.path.splitext(p)[0] + '.jpg'
    output_img_path = os.path.join(output_dir, output_img_name)
    
    input_img = Image.open(input_img_path)
    output_img = input_img.convert('RGB')
    output_img.save(output_img_path, quality=40)

    file_size = os.path.getsize(output_img_path)
    print(f"Converted {p} to {output_img_name}, Size: {file_size / 1024:.2f} KB")


print("finished")
