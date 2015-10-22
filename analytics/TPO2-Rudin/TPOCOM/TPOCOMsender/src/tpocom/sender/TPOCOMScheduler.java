package tpocom.sender;

import java.rmi.RemoteException;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

import communicator.TPOCOMcommunicator;

import spms.run.rudin.xmltool.XmlToolException;

/**
 * This class is used to schedule the tasks of TPOCOM Sender.
 * @author vivek
 *
 */
public class TPOCOMScheduler {
	
	/**
	 * TPOCOMScheduler takes in the TaskRunner and HeartBeatMessenger which
	 * are to be repeatedly scheduled. It also opens Connection to the endpoint 
	 * using TPOCOMcommunicator before scheduling
	 * @param taskRunner
	 * @param hbm
	 * @param tpocom
	 * @param taskRunInterval
	 * @param heartBeatInterval
	 */
	public TPOCOMScheduler(TaskRunner taskRunner, HeartBeatMessenger hbm,
			TPOCOMcommunicator tpocom, int taskRunInterval,
			int heartBeatInterval) {
		this.taskRunner = taskRunner;
		this.hbm = hbm;
		this.taskRunInterval = taskRunInterval;
		this.heartBeatInterval = heartBeatInterval;
		this.fScheduler = Executors.newScheduledThreadPool(2);
		this.tpocom = tpocom;
	}
	
	/**
	 * Schedules the TaskRunner and the HeartBeatMessenger
	 * @throws RemoteException
	 * @throws XmlToolException
	 */
	public void ScheduleRepeatTask() throws RemoteException, XmlToolException {
		this.tpocom.connect();
		this.futureTaskHandle = fScheduler.scheduleWithFixedDelay(
				this.taskRunner, 0, this.taskRunInterval, TimeUnit.SECONDS);
		this.HeartBeatTaskHandle = fScheduler.scheduleAtFixedRate(this.hbm, 0,
				this.heartBeatInterval, TimeUnit.SECONDS);
	}
	
	/**
	 * This method stops all the scheduled tasks
	 */
	public void StopScheduledTasks() {
		this.futureTaskHandle.cancel(false);
		this.HeartBeatTaskHandle.cancel(false);
		fScheduler.shutdown();
	}

	private final ScheduledExecutorService fScheduler;
	private TaskRunner taskRunner;
	private HeartBeatMessenger hbm;
	private int taskRunInterval;
	private int heartBeatInterval;
	private TPOCOMcommunicator tpocom;
	private ScheduledFuture<?> futureTaskHandle;
	private ScheduledFuture<?> HeartBeatTaskHandle;
}
