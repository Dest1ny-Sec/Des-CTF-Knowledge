# 2023 年安询杯 ez_cpp 题解

> 原文: https://www.ctfiot.com/119444.html
> ID: 119444


```
// Enc1
 int tmp_result;
 for (int i = 0; i < 32; i++) {
 bool find_v3 = false;
 for (int v3 = 0; v3 < 128; v3++) {
 int result;
 if ((v3 - 61) <= 0x3Eu) {
 result = v3;
 int v7 = v3 + 13;
 if (v3 > 90) {
 if (v7 <= 122)
 tmp_result = v3 + 13;
 else
 tmp_result = v3 - 13;
 } else {
 result = -13;
 if (v7 <= 90)
 result = 13;
 result = v3 + result;
 tmp_result = result;
 }
 }

 if (tmp_result == arr[i] && check(v3)) {
 find_v3 = true;
 cout << (char)v3;
 }
 }
 if (!find_v3) {
 cout << (char)arr[i];
 }
 cout << " ";
 }
    #include 
using namespace std;

unsigned int dec3(unsigned int a1) {
 unsigned int a2 = 8;
 a1--;

 unsigned int v2; // edx
 unsigned int v3; // edi
 unsigned int v4; // ebx

 v2 = 0;
 v3 = 0;
 if (a2 > 0) {
 v4 = a2 - 1;
 do
 v2 |= ((a1 >> v3++) & 1) << v4--;
 while (v3 < a2);
 }
 return v2;
}

unsigned int arr[] = {0x22, 0x0FFFFFFA2, 0x72, 0x0FFFFFFE6,
 0x52, 0x0FFFFFF8C, 0x0FFFFFFF2, 0x0FFFFFFD4,
 0x0FFFFFFA6, 0x0A, 0x3C, 0x24,
 0x0FFFFFFA6, 0x0FFFFFF9C, 0x0FFFFFF86, 0x24,
 0x42, 0x0FFFFFFD4, 0x22, 0x0FFFFFFB6,
 0x14, 0x42, 0x0FFFFFFCE, 0x0FFFFFFAC,
 0x14, 0x6A, 0x2C, 0x7C,
 0x0FFFFFFE4, 0x0FFFFFFE4, 0x0FFFFFFE4, 0x1E};

void dec2(unsigned int *arr) {
 int v6[] = {0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1,
 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0};

 int index = 0;
 unsigned int result;
 do {
 if (index <= 16) {
 if (index >= 16) {
 arr[index] ^= 4;
 } else {
 result = v6[index];
 if (result) {
 if (!--result)
 arr[index] ^= 9;
 } else {
 arr[index] += 2;
 }
 }
 } else {
 result = v6[index];
 if (result) {
 if (!--result)
 arr[index] ^= 6;
 } else {
 arr[index] += 5;
 }
 }
 ++index;
 } while (arr[index]);
}

int check(int c) {
 if ((c >= 'a' && c <= 'z') (c >= 'A' && c <= 'Z')
 (c >= '0' && c <= '9') c == '{' c == '}' || c == '_') {
 return true;
 }
 return false;
}

int main() {
 // Enc3
 for (int i = 0; i < 32; i++) {
 arr[i] ^= 1;
 arr[i] = dec3(arr[i]);
 }

 // Enc2
 dec2(arr);

 // Enc1
 int tmp_result;
 for (int i = 0; i < 32; i++) {
 bool find_v3 = false;
 for (int v3 = 0; v3 < 128; v3++) {
 int result;
 if ((v3 - 61) <= 0x3Eu) {
 result = v3;
 int v7 = v3 + 13;
 if (v3 > 90) {
 if (v7 <= 122)
 tmp_result = v3 + 13;
 else
 tmp_result = v3 - 13;
 } else {
 result = -13;
 if (v7 <= 90)
 result = 13;
 result = v3 + result;
 tmp_result = result;
 }
 }

 if (tmp_result == arr[i] && check(v3)) {
 find_v3 = true;
 cout << (char)v3;
 }
 }
 if (!find_v3) {
 cout << (char)arr[i];
 }
 cout << " ";
 }

 return 0;
}
```
