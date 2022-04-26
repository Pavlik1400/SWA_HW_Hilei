# SWA_HW2

You can find in 'videos' a presentations where I present task 3, 4, 5, console outputs and how to use code in the repository

- **Task 3 comments**: Hazelcast by default has guarantees that when 1 node dies, data is not lost. So as I show in the video, when I kill one instance - data is no lost. When I kill second instance after some time, enough to restore backup, data is also not lost. But when I kill 2 nodes quickly one after another - data is lost. 
- **Task 4 comments**: No locking is not safe, and multi-processing counter doesn't work as expected. Optimistic/Pesimistic approaches can solve this problem.
- **Task 5 comments**: When there are 2 consumers, they can read quicker than 1 producer produces data. When consumers are killed, after queue is filled, producer is locked. And vice versa - when producer is killed, consumers are locked until someone starts pushing to queue. Also I didn't find any pattern of how 2 consumers pull values from queue.