# 问题

可以完成cursor的大部分代码生成功能

完成UOS unittest需要：

方案一： 对于每一个unittest，提供一个list， 包括相关的class定义，等待测试的代码
        1. pre-defined unittest task： 目前的实现是预先定义一个task
        2. 实现预定义task 保存，加载功能

方案二： 在planner上进行操作
        1. 在每一步允许user进行调整
        2. meta prompt进行推广example到复杂的多次repeat的task

另一方面：

planner生成的是否需要一个graph

feat:
    1. 重排task，修改其中的某一步
    2. task推广，重复做一个task，修改一个flow后，可以推广到剩余的flow
    3. 命令 /save, /load, /clear, /exit等， planner确认，调整
    4. save & reload task,: /save $task_name, /load $task_name $args