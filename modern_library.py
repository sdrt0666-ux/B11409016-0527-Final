import os
import atexit

class LegacyLibrarySystem:
    def __init__(self, file_name="lib_data.txt"):
        self.file_name = file_name
        self.books = []  # 替代原本的 d2，儲存圖書清單
        self.load_books_from_file()
        
        # 註冊自動存檔機制，確保不論如何退出都會保存記憶體資料
        atexit.register(self.save_books_to_file)

    def load_books_from_file(self):
        """從文字檔案載入圖書資料並解析特殊格式 (@@ 與 ##)"""
        if not os.path.exists(self.file_name):
            print("資料檔案不存在，將在退出時建立新檔。")
            return

        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 解析原始格式：書名@@ISBN##狀態
                    primary_split = line.split("@@")
                    if len(primary_split) == 2:
                        title = primary_split[0]
                        secondary_split = primary_split[1].split("##")
                        if len(secondary_split) == 2:
                            isbn = secondary_split[0]
                            status = secondary_split[1]
                            self.books.append({"title": title, "isbn": isbn, "status": status})
            print("資料載入成功！")
        except Exception as e:
            print(f"讀取檔案時發生錯誤: {e}")

    def save_books_to_file(self):
        """將記憶體中的圖書資料以原始格式寫回文字檔案"""
        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                for book in self.books:
                    # 還原格式：書名@@ISBN##狀態
                    f.write(f"{book['title']}@@{book['isbn']}##{book['status']}\n")
            print("\n資料已安全儲存到檔案！")
        except Exception as e:
            print(f"儲存檔案時發生錯誤: {e}")

    def is_isbn_exists(self, isbn):
        """檢查特定 ISBN 是否已存在於系統中"""
        return any(book["isbn"] == isbn for book in self.books)

    def add_book(self, title, isbn, status):
        """新增一本書到記憶體清單"""
        if self.is_isbn_exists(isbn):
            print("ISBN Exist")
            return
        
        self.books.append({"title": title, "isbn": isbn, "status": status})
        print("Success")

    def show_all_books(self):
        """顯示目前所有圖書"""
        if not self.books:
            print("目前沒有任何圖書資料。")
            return
        for book in self.books:
            print(f"書名: {book['title']}, ISBN: {book['isbn']}, 狀態: {book['status']}")

    def borrow_book(self, isbn):
        """根據 ISBN 將圖書狀態改為 borrowed"""
        for book in self.books:
            if book["isbn"] == isbn:
                book["status"] = "borrowed"
                print("Updated")
                return
        print("ISBN Not Found")

    def run(self):
        """主程式互動迴圈"""
        print("=== 圖書管理系統 v1.0 (重構模組化版) ===")
        while True:
            try:
                op = input("> ").strip()
                
                if op == "exit":
                    print("系統關閉中...")
                    break
                    
                elif op.startswith("add "):
                    raw = op[4:].split("/")
                    if len(raw) == 3:
                        # 傳入去空白後的 書名, ISBN, 狀態
                        self.add_book(raw[0].strip(), raw[1].strip(), raw[2].strip())
                    else:
                        print("Format Error")
                        
                elif op == "show":
                    self.show_all_books()
                    
                elif op.startswith("borrow "):
                    isbn = op[7:].strip()
                    self.borrow_book(isbn)
                    
                elif not op:
                    continue
                else:
                    print("Unknown Command")
                    
            except (KeyboardInterrupt, EOFError):
                print("\n偵測到強制結束訊號，正在安全退出...")
                break

if __name__ == "__main__":
    library = LegacyLibrarySystem()
    library.run()