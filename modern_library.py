import os
import json
import atexit

class JsonLibrarySystem:
    def __init__(self, file_name="lib_data.json"):
        self.file_name = file_name
        self.books = []  # 儲存結構：[{"title": "...", "isbn": "...", "status": "..."}, ...]
        self.load_books_from_json()
        
        # 註冊自動存檔機制
        atexit.register(self.save_books_to_json)

    def load_books_from_json(self):
        """從 JSON 檔案載入圖書資料，包含完整的錯誤處理"""
        if not os.path.exists(self.file_name):
            print(f"提示：檔案 '{self.file_name}' 不存在，系統將在退出時自動建立。")
            return

        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                self.books = json.load(f)
                # 確保載入的資料一定是 list 格式，防範手動改檔造成的格式錯誤
                if not isinstance(self.books, list):
                    print("警告：JSON 根節點格式錯誤（應為列表），已初始化為空清單。")
                    self.books = []
                else:
                    print(f"成功載入 {len(self.books)} 筆圖書資料！")
        except json.JSONDecodeError:
            print("錯誤：JSON 檔案格式損毀或解析失敗！將使用空白資料庫執行，退出時將覆蓋原檔。")
            self.books = []
        except PermissionError:
            print("錯誤：權限不足，無法讀取圖書檔案。")
        except Exception as e:
            print(f"讀取檔案時發生未預期的錯誤: {e}")

    def save_books_to_json(self):
        """將記憶體中的圖ша資料以標準 JSON 格式寫回檔案"""
        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                # 使用 indent=4 讓 JSON 檔案易於人類閱讀，ensure_ascii=False 確保中文不變成亂碼
                json.dump(self.books, f, ensure_ascii=False, indent=4)
            print("\n[系統通知] 資料已安全儲存至 JSON 檔案！")
        except PermissionError:
            print("\n[儲存失敗] 錯誤：權限不足，無法寫入檔案。")
        except Exception as e:
            print(f"\n[儲存失敗] 儲存檔案時發生未預期的錯誤: {e}")

    def is_isbn_exists(self, isbn):
        """檢查特定 ISBN 是否已存在"""
        return any(book["isbn"] == isbn for book in self.books)

    def add_book(self, title, isbn, status):
        """新增圖書"""
        if self.is_isbn_exists(isbn):
            print(f"新增失敗：ISBN '{isbn}' 已經存在。")
            return
        
        self.books.append({"title": title, "isbn": isbn, "status": status})
        print(f"成功新增圖書：《{title}》 (已暫存於記憶體)")

    def show_all_books(self):
        """顯示目前所有圖書"""
        if not self.books