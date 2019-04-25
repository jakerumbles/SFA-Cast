# SFA-Cast
UDP multicast client/server application for sharing your screen with the classroom.

With this program, students will be able to see what the professor is doing on their screen with a mirror copy on their monitors.

Screenshot function:
-There is a pygame "button"
-Pressing f12 will also take a screenshot

Notes from Dr. Glendowne:
-Is this solely for video broadcasting? Are there any other interactions it might enable (screenshots for example?)
    I responded yes for now and that we may attempt to implement a screenshot function after the fact.
Is communication one way? (Can the server receive data/screen video from the clients?)
    I also said yes.
** You should consider compressing the stream and test how the compression (or lack thereof) impacts the performance
    This is something we should look into.
