using System;
using System.Text;

class MainClass
{
    static int clicks = 0;

    static void Page()
    {
        Console.WriteLine("{\"type\":\"page\",\"title\":\"C# 插件\",\"elements\":["
            + "{\"kind\":\"text\",\"label\":\"这个页面由 C# 子进程生成\"},"
            + "{\"kind\":\"text\",\"label\":\"点击次数：" + clicks + "\"},"
            + "{\"kind\":\"button\",\"id\":\"click\",\"label\":\"点我\"},"
            + "{\"kind\":\"button\",\"id\":\"close\",\"label\":\"返回\"}"
            + "]}");
    }

    static void Main()
    {
        Console.OutputEncoding = Encoding.UTF8;
        string line;
        while ((line = Console.ReadLine()) != null)
        {
            if (line.Contains("\"type\":\"open\""))
            {
                Page();
            }
            else if (line.Contains("\"type\":\"action\""))
            {
                if (line.Contains("\"id\":\"close\""))
                {
                    Console.WriteLine("{\"type\":\"close\"}");
                    return;
                }
                if (line.Contains("\"id\":\"click\""))
                {
                    clicks += 1;
                }
                Page();
            }
        }
    }
}
