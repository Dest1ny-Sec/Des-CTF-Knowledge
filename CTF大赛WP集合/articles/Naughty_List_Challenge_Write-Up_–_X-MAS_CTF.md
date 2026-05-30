# Naughty List Challenge Write-Up – X-MAS CTF

> 原文: https://www.ctfiot.com/87572.html
> ID: 87572

naughty_list.cppThis C++ program is a simple command-line application that allows the user to perform several actions:

Ask PinkiePie for the flag: if the “PinkiePie” entry is present in the naughty_list unordered map, the program will output a message saying that PinkiePie will not tell you the flag. Otherwise, the program will open the file flag.txt and output its contents.

Query the naughty list: the user is prompted to enter a name, and the program will check whether the name is present in the naughty_list unordered map.

Add a name to the naughty list: the user is prompted to enter a name, and the program will add the name to the naughty_list unordered map with the value “Naughty”. However, if the unordered map is already at its maximum size (defined by the constant ELF_MAX_NAUGHTY_COUNT), the program will prevent adding a new item.

C++ unordered map

The entire challenge revolves around the C++ unordered map.

An unordered map is an associative container that contains key-value pairs with unique keys. Internally, the elements are not sorted in any particular order but are organized into buckets. Which bucket an element is placed into depends entirely on the hash of its key. – en.cppreference.com

I’ve made an instrumented version of the source code to print the content of the map:

template<typename K, typename V>

void print_map(std::unordered_map<K, V> const &m)

{

for (auto const &pair: m) {

 std::cout << “{“ << pair.first << “: “ << pair.second << “}\n”;

}

}

[Truncated]

case 1:

{

ask_pinkiepie();

print_map(naughty_list);

}

[Truncated]

Playing a bit with it, adding 10 elements and printing the content of the list, a “weird” pattern began to appear:

{11: Naughty}

{10: Naughty}

{9: Naughty}

{8: Naughty}

{7: Naughty}

{6: Naughty}

{4: Naughty}

{5: Naughty}

{3: Naughty}

{1: Naughty}

{2: Naughty}

As you can see, the elements in the list occupy a “random” spot; the “unordered” keyword in the unordered_map‘s name should tell you something…

Unordered associative data structures don’t give you any guarantee on element order. Rehashing invalidates the iterator and might cause the elements to be re-arranged in different buckets but it doesn’t invalidate references to the elements.

In the case of “Insert”/”Erase” operations, depending on different factors, iterators are invalidated when rehashing occurs.

With that in mind, it was evident that I needed to push the “PinkiePie” element “out of the list”.

Removing PinkiePie

Since the check for “PinkiePie” presence is made only on the first 16 elements of the list:

#define ELF_MAX_NAUGHTY_COUNT 16

[Truncated]

for (int i = 0; i < ELF_MAX_NAUGHTY_COUNT; i++)

{

if (it->first == “PinkiePie”)

{

 pinkiepie_naughty = true;

break;

}

 ++it;

if (it == naughty_list.end())

{

break;

}

}

If we can find a way to add enough elements to the list, causing the elements to be re-arranged in a way that “PinkiePie” doesn’t sit in the first 16 spots, the program will happily print out the flag.

The main problem is that we cannot have more than 16 elements in the list as the check, in the add_to_list() function, will prevent us from adding more items:

 

if (naughty_list.size() == ELF_MAX_NAGHTY_COUNT){

The square bracket operator

Luckily enough, the is_naughty() function use the square bracket operator:

bool is_naughty(const std::string &name) { return !(naughty_list[name] == “”); }

The function uses the square bracket operator ([]) to access the value associated with the key name in the map. If the key is present in the map, the operator returns the corresponding value. If the key is not present in the map, the operator will insert a new entry into the map with the key name and the default value for the value type (an empty string in this case).

For example, if the naughty_list unordered map is initially empty and the is_naughty() function is called with the parameter “Rudolph”, the function will insert a new entry into the map with the key “Rudolph” and the default value (in this case an empty string): {"Rudolph", ""}

It’s important to note that the behaviour of the square bracket operator is a general feature of C++, including maps and unordered maps. If you want to check whether a key is present in an unordered map without modifying the map, you can use the count()/find()/contains() member functions instead.

POC

I’ve then proceeded to add all the items possible via the add_to_list() function, and then, using the is_naughty() to add enough items to cause the “PinkiePie” item to be “pushed out” of the first 16 spots:

PinkiePie is satisfied. Here is your flag!

X-MAS{PiNKi3pi3_wiLl_n07_r3C3IV3_C04l_7hI5_y34R}

References

X-MAS CTF 2022

htsp.ro Team

https://en.cppreference.com/w/cpp/container/unordered_map