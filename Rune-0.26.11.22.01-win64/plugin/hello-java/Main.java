import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

public class Main {
    static int clicks = 0;

    static void page(PrintStream out) {
        out.println("{\"type\":\"page\",\"title\":\"Java 插件\",\"elements\":["
                + "{\"kind\":\"text\",\"label\":\"这个页面由 Java 子进程生成\"},"
                + "{\"kind\":\"text\",\"label\":\"点击次数：" + clicks + "\"},"
                + "{\"kind\":\"button\",\"id\":\"click\",\"label\":\"点我\"},"
                + "{\"kind\":\"button\",\"id\":\"close\",\"label\":\"返回\"}"
                + "]}");
    }

    public static void main(String[] args) throws Exception {
        PrintStream out = new PrintStream(System.out, true, "UTF-8");
        BufferedReader in = new BufferedReader(
                new InputStreamReader(System.in, StandardCharsets.UTF_8));
        String line;
        while ((line = in.readLine()) != null) {
            if (line.contains("\"type\":\"open\"")) {
                page(out);
            } else if (line.contains("\"type\":\"action\"")) {
                if (line.contains("\"id\":\"close\"")) {
                    out.println("{\"type\":\"close\"}");
                    return;
                }
                if (line.contains("\"id\":\"click\"")) {
                    clicks += 1;
                }
                page(out);
            }
        }
    }
}
