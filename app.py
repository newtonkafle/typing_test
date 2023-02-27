from interface import AppInterface
import json

if __name__ == "__main__":
    app = AppInterface()
    app.mainloop()

    # with open('data.json', 'r') as data:
    #     lessons = json.load(data)


# for num, lesson in enumerate(lessons):
#     print(lesson)
#     key = f'lesson_{num+1}'
#     lesson[key] = lesson.pop('Lesson_1')
#     print(lesson)

# json_object = json.dumps(lessons, indent=3)

# with open('data.json', 'w') as data:
#     data.write(json_object)
#     print('.........done')

# going to make an typing test application
# should show the sentences to type
# should color the character after you type correct or wrong
# should be able to go to the next lesson
# should be able to see the speed and accuracy
