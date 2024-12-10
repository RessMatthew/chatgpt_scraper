1. 路线1：

   1. 新打开 Chrome for Test
   2. 需要在 `https://chat.openai.com/auth/login`，输入邮箱/密码登入
   3. ==有邮箱验证这个棘手的问题==。

   路线2：（最终采用）

   1. 连接到已打开的 Chrome浏览器，利用 session 绕过登入。
   2. 读取 input 目录下的每个文件作为prompt
   3. 将 response 存入到output，文件名与输入文件对应。

   ```
   我的目标：
   连接到已经打开的Chrome浏览器
   爬取https://chatgpt.com/

   工具要求：
   python, selenium, Chrome浏览器, ChromeDriver

   步骤：
   1. 连接到已经打开的Chrome浏览器，访问https://chatgpt.com/
   2. 爬取页面内容
   ```
   ## 用户手册

   ### 在 debugging-port=9222 端口打开 chrome，便于连接到已经打开的Chrome浏览器


   ```
   # Windows
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222

   # Mac
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

   # Linux
   google-chrome --remote-debugging-port=9222
   ```
