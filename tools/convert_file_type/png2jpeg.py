from PIL import Image
import os
import datetime

sample_dir = os.path.join(os.getcwd(), 'sample')

# 出力ディレクトリが存在しない場合は作成
if not os.path.exists(sample_dir):
    os.makedirs(sample_dir)

# 指定ディレクトリのファイルを取得
files = os.listdir(sample_dir)
print(f"files: {files}")

# 取得したファイルからPNGファイルのみ取得
pngs = [f for f in files if f.lower().endswith('.png')]

# 出力ファイル名用に現在時刻の取得
dt_now = datetime.datetime.now().strftime('%y%m%d_%H%M%S')

# pngをjpgに変換する
for p in pngs:
    png_path = os.path.join(sample_dir, p)
    img_file_name = os.path.splitext(p)[0] + '.jpg'
    img_path = os.path.join(sample_dir, img_file_name)
    
    input_img = Image.open(png_path)
    output_img = input_img.convert('RGB')
    output_img.save(img_path, quality=40)

    file_size = os.path.getsize(img_path)
    print(f"Converted {p} to {img_file_name}, Size: {file_size / 1024:.2f} KB")

    os.remove(png_path)
    print(f"Removed {p}")

print("finished")
