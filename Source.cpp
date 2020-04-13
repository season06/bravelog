#include<iostream>
#include<string>
#include<vector>
using namespace std;
456
class Student
{
public:
	bool Insert(string, string, string);
	bool Delete(string, string, string);
	bool Search(string, string, string);
	bool Print();
	bool is_number(string);
private:
	vector<string> firstName;
	vector<string> lastName;
	vector<string> phone;
	int length = 0;
};
bool Student::Insert(string first, string last, string ph)
{
	// 如果長度超出範圍、phone不是數字、insert長度超過10，回傳false
	if (first.length() > 25 || last.length() > 30 || ph.length() > 15 || is_number(ph) == false || length >= 10)
		return false;
	// 如果存在相同的資料, 回傳false
	for (int i = 0; i < length; i++)
	{
		if (first == firstName[i] && last == lastName[i] && ph == phone[i])
			return false;
	}
	// 如果insert成功, 長度+1, 輸出資料並回傳true
	firstName.push_back(first);
	lastName.push_back(last);
	phone.push_back(ph);
	length++;
	return true;	
}
bool Student::Delete(string first, string last, string ph)
{
	// 如果有找到且刪除, 長度-1, 回傳true
	for (int i = 0; i < length; i++)
	{
		if (first == firstName[i] && last == lastName[i] && ph == phone[i])
		{
			firstName.erase(firstName.begin() + i);
			lastName.erase(lastName.begin() + i);
			phone.erase(phone.begin() + i);
			length--;
			return true;
		}
	}
	return false; // 如果沒有找到, 回傳false
}
bool Student::Search(string first, string last, string ph)
{
	for (int i = 0; i < length; i++)
	{
		if (first == firstName[i] && last == lastName[i] && ph == phone[i])
		{
			cout << i << "\n";
			return true; // 如果有找到且刪除, 回傳true
		}
	}
	return false; // 如果沒有找到, 回傳false
}
bool Student::Print()
{
	// 如果陣列裡沒有資料, 回傳false
	if(length == 0)
		return false;
	// 全部輸出後, 回傳true
	for (int i = 0; i < length; i++)
		cout << firstName[i] << " " << lastName[i] << " " << phone[i] << "\n";
	return true;
}
bool Student::is_number(string phone)
{
	for (int i = 0; i < phone.length(); i++)
	{
		// 0~9 的 ASCII碼為 48~57
		if (phone[i] < 48 || phone[i]>57)
			return false;
	}
	return true;
}
int main()
{
	string command;
	Student stu;
	while (cin >> command)
	{
		string firstName, lastName, phone;
		if (command == "insert")
		{
			cin >> firstName >> lastName >> phone;
			bool ck = stu.Insert(firstName, lastName, phone);
			if (ck == false)
				cout << "Insert Error\n";
		}
		else if (command == "delete")
		{
			cin >> firstName >> lastName >> phone;
			bool ck = stu.Delete(firstName, lastName, phone);
			if (ck == false)
				cout << "Delete Error\n";
		}
		else if (command == "search")
		{
			cin >> firstName >> lastName >> phone;
			bool ck = stu.Search(firstName, lastName, phone);
			if (ck == false)
				cout << "Search Error\n";
		}
		else if (command == "print")
		{
			bool ck = stu.Print();
			if (ck == false)
				cout << "Print Error\n";
		}
		else
		{
			cout << "Input Error\n";
		}
	}
	return 0;
}