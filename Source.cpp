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
	// �p�G���׶W�X�d��Bphone���O�Ʀr�Binsert���׶W�L10�A�^��false
	if (first.length() > 25 || last.length() > 30 || ph.length() > 15 || is_number(ph) == false || length >= 10)
		return false;
	// �p�G�s�b�ۦP�����, �^��false
	for (int i = 0; i < length; i++)
	{
		if (first == firstName[i] && last == lastName[i] && ph == phone[i])
			return false;
	}
	// �p�Ginsert���\, ����+1, ��X��ƨæ^��true
	firstName.push_back(first);
	lastName.push_back(last);
	phone.push_back(ph);
	length++;
	return true;	
}
bool Student::Delete(string first, string last, string ph)
{
	// �p�G�����B�R��, ����-1, �^��true
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
	return false; // �p�G�S�����, �^��false
}
bool Student::Search(string first, string last, string ph)
{
	for (int i = 0; i < length; i++)
	{
		if (first == firstName[i] && last == lastName[i] && ph == phone[i])
		{
			cout << i << "\n";
			return true; // �p�G�����B�R��, �^��true
		}
	}
	return false; // �p�G�S�����, �^��false
}
bool Student::Print()
{
	// �p�G�}�C�̨S�����, �^��false
	if(length == 0)
		return false;
	// ������X��, �^��true
	for (int i = 0; i < length; i++)
		cout << firstName[i] << " " << lastName[i] << " " << phone[i] << "\n";
	return true;
}
bool Student::is_number(string phone)
{
	for (int i = 0; i < phone.length(); i++)
	{
		// 0~9 �� ASCII�X�� 48~57
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