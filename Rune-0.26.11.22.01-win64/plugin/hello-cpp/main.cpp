#include <iostream>
#include <string>

static int clicks = 0;

static void page() {
    std::cout
        << "{\"type\":\"page\",\"title\":\"C++ 插件\",\"elements\":["
        << "{\"kind\":\"text\",\"label\":\"这个页面由 C++ 子进程生成\"},"
        << "{\"kind\":\"text\",\"label\":\"点击次数：" << clicks << "\"},"
        << "{\"kind\":\"button\",\"id\":\"click\",\"label\":\"点我\"},"
        << "{\"kind\":\"button\",\"id\":\"close\",\"label\":\"返回\"}"
        << "]}" << std::endl;
}

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        if (line.find("\"type\":\"open\"") != std::string::npos) {
            page();
        } else if (line.find("\"type\":\"action\"") != std::string::npos) {
            if (line.find("\"id\":\"close\"") != std::string::npos) {
                std::cout << "{\"type\":\"close\"}" << std::endl;
                return 0;
            }
            if (line.find("\"id\":\"click\"") != std::string::npos) {
                clicks += 1;
            }
            page();
        }
    }
    return 0;
}
