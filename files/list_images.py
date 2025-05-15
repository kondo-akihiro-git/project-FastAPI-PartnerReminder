import os

# 対象のディレクトリパスを指定
target_path = "/Users/aki/PartnerReminder/backend/files/test_outer_images"

# 対象の拡張子（小文字で指定）
image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

def list_image_files(path):
    try:
        files = os.listdir(path)
        images = [f for f in files if os.path.isfile(os.path.join(path, f)) and os.path.splitext(f)[1].lower() in image_extensions]
        print("画像ファイル一覧:")
        for img in images:
            name, ext = os.path.splitext(img)
            print(f"ファイル名: {name}, 拡張子: {ext}")
    except FileNotFoundError:
        print(f"指定されたパスが見つかりません: {path}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

# 実行
if __name__ == "__main__":
    list_image_files(target_path)
