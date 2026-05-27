import os
import json
import atexit

class OptimizedJsonLibrarySystem:
    def __init__(self, file_name="lib_data.json"):
        self.file_name = file_name
        self.books = []  # 所有資料都暫存在這個記憶體 List 中
        self.load_books_from_json()  # 初始化時唯一次的讀取
        
        # 核心優化：註冊自動防禦機制，程式「關閉時」才一次性寫入硬碟
        atexit.register(self.save_books_to_json)

    def load_books_from_json(self):
        """唯一次讀取硬碟：將整份資料庫載入到記憶體"""
        if not os.path.exists(self.file_name):
            print(f"提示：檔案 '{self.file_name}' 不存在，系統將在退出時自動建立。")
            return

        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                self.books = json.load(f)
                if not isinstance(self.books, list):
                    print("警告：JSON 格式異常，已重設為空清單。")
                    self.books = []
                else:
                    print(f"資料載入成功！目前記憶體中有 {len(self.books)} 筆館藏。")
        except (json.JSONDecodeError, Exception) as e:
            print(f"讀取或解析檔案時發生錯誤 ({e})，啟動空白系統。")
            self.books = []

    def save_books_to_json(self):
        """唯一次寫入硬碟：在程式關閉時，將記憶體資料一口氣同步回硬碟"""
        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
            print("\n[效能優化通知] 記憶體中的所有變更，已在系統關閉前一次性儲存至 JSON 檔案！")
        except Exception as e:
            print(f"\n[儲存失敗] 寫入檔案時發生未預期的錯誤: {e}")

    def is_isbn_exists(self, isbn):
        """在記憶體中查找 ISBN"""
        return any(book["isbn"] == isbn for book in self.books)

    def add_book(self, title, isbn, status):
        """【記憶體操作】新增圖書：完全不碰硬碟"""
        if self.is_isbn_exists(isbn):
            print(f"新增失敗：ISBN '{isbn}' 已經存在。")
            return
        
        # 僅操作記憶體變數，速度極快
        self.books.append({"title": title, "isbn": isbn, "status": status})
        print(f"成功新增圖書：《{title}》 (已暫存於記憶體)")

    def show_all_books(self):
        """【記憶體操作】讀取目前暫存的館藏"""
        if not self.books:
            print("目前館藏空空如也。")
            return
        
        print(f"\n--- 目前館藏清單 (共 {len(self.books)} 本) ---")
        for idx, book in enumerate(self.books, 1):
            print(f"{idx}. 書名: {book['title']} | ISBN: {book['isbn']} | 狀態: {book['status']}")
        print("-" * 35)

    def borrow_book(self, isbn):
        """【記憶體操作】借閱圖書：完全不碰硬碟"""
        for book in self.books:
            if book["isbn"] == isbn:
                if book["status"].lower() == "borrowed":
                    print("提示：此書目前已經是被借出狀態。")
                else:
                    book["status"] = "borrowed"  # 僅修改記憶體中的欄位
                    print(f"成功借閱：《{book['title']}》！(已更新記憶體)")
                return
        print(f"借閱失敗：找不到 ISBN 為 '{isbn}' 的圖書。")

    def run(self):
        """主程式互動迴圈"""
        print("=== 圖書管理系統 v3.0 (高乘載記憶體優化版) ===")
        
        while True:
            try:
                op = input("> ").strip()
                if op == "exit":
                    print("正在關閉系統...")
                    break  # 離開迴圈後，會由 atexit 機制觸發 save_books_to_json
                    
                elif op.startswith("add "):
                    argument_part = op[4:].strip()
                    if not argument_part:
                        print("格式錯誤！正確格式為：add 書名/ISBN/狀態")
                        continue
                        
                    raw = argument_part.split("/")
                    if len(raw) == 3 and all(field.strip() for field in raw):
                        self.add_book(raw[0].strip(), raw[1].strip(), raw[2].strip())
                    else:
                        print("格式錯誤！請確保欄位完整且使用 '/' 分隔。")
                        
                elif op == "show":
                    self.show_all_books()
                    
                elif op.startswith("borrow "):
                    isbn = op[7:].strip()
                    if isbn:
                        self.borrow_book(isbn)
                    else:
                        print("格式錯誤！請輸入 ISBN 碼。")
                        
                elif not op:
                    continue
                else:
                    print("未知指令！")
                    
            except (KeyboardInterrupt, EOFError):
                print("\n偵測到強制結束訊號，正在安全退出...")
                break

if __name__ == "__main__":
    library = OptimizedJsonLibrarySystem()
    library.run()