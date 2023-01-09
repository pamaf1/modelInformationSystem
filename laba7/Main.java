import PetriObj.PetriObjModel;
import PetriObj.PetriSim;
import LibNet.NetLibrary;
import PetriObj.ExceptionInvalidTimeDelay;
import PetriObj.ExceptionInvalidNetStructure;
import java.util.ArrayList;

public class Main {

    public static void main(String args[]) {
        double timeModeling = 10000;
            try {
            PetriObjModel model = busStationModel(15);
            model.go(timeModeling);
            model.printStatistics();
        } catch(Exception ex) {
            System.out.println(ex);
        }
    }

    public static PetriObjModel roboticSystemModel1() throws ExceptionInvalidTimeDelay, ExceptionInvalidNetStructure{
        ArrayList<PetriSim> list = new ArrayList<>();
        list.add(new PetriSim(NetLibrary.CreateNetGenerator(40.0, 1, "exp")));
        list.add(new PetriSim(NetLibrary.robotTakingAction(1, 1, Integer.toString(1))));
        list.add(new PetriSim(NetLibrary.robotTransportingAction(1, 6, Integer.toString(1))));
        list.add(new PetriSim(NetLibrary.robotPutAction(1, 1, Integer.toString(1))));
        list.add(new PetriSim(NetLibrary.robotTransportingAction(1, 1, "First comeback")));
        list.add(new PetriSim(NetLibrary.firstStation(60)));

        list.get(0).getNet().getListP()[1] = list.get(1).getNet().getListP()[0];
        list.get(1).getNet().getListP()[2] = list.get(2).getNet().getListP()[0];
        list.get(2).getNet().getListP()[1] = list.get(3).getNet().getListP()[0];
        list.get(3).getNet().getListP()[2] = list.get(4).getNet().getListP()[0];
        list.get(1).getNet().getListP()[1] = list.get(4).getNet().getListP()[1];
        list.get(3).getNet().getListP()[1] = list.get(5).getNet().getListP()[0];

        list.add(new PetriSim(NetLibrary.robotTakingAction(1, 1, Integer.toString(2))));
        list.add(new PetriSim(NetLibrary.robotTransportingAction(1, 7, Integer.toString(2))));
        list.add(new PetriSim(NetLibrary.robotPutAction(1, 1, Integer.toString(2))));
        list.add(new PetriSim(NetLibrary.robotTransportingAction(1, 1, "Second comeback")));
        list.add(new PetriSim(NetLibrary.secondStation(100))); 

        list.get(5).getNet().getListP()[1] = list.get(6).getNet().getListP()[0];
        list.get(6).getNet().getListP()[2] = list.get(7).getNet().getListP()[0];
        list.get(7).getNet().getListP()[1] = list.get(8).getNet().getListP()[0];
        list.get(8).getNet().getListP()[2] = list.get(9).getNet().getListP()[0];
        list.get(9).getNet().getListP()[1] = list.get(6).getNet().getListP()[1];
        list.get(8).getNet().getListP()[1] = list.get(10).getNet().getListP()[0];

        list.add(new PetriSim(NetLibrary.robotTakingAction(1, 1, Integer.toString(3))));
        list.add(new PetriSim(NetLibrary.robotTransportingAction(1, 5, Integer.toString(3))));
        list.add(new PetriSim(NetLibrary.robotPutAction(1, 1, Integer.toString(3))));
        list.add(new PetriSim(NetLibrary.robotTransportingAction(1, 1, "Third comeback")));

        list.get(10).getNet().getListP()[1] = list.get(11).getNet().getListP()[0];
        list.get(11).getNet().getListP()[2] = list.get(12).getNet().getListP()[0];
        list.get(12).getNet().getListP()[1] = list.get(13).getNet().getListP()[0];
        list.get(13).getNet().getListP()[2] = list.get(14).getNet().getListP()[0];
        list.get(14).getNet().getListP()[1] = list.get(11).getNet().getListP()[1];

        PetriObjModel model = new PetriObjModel(list);
        return model;
    }

    public static PetriObjModel roboticSystemModel2() throws ExceptionInvalidTimeDelay, ExceptionInvalidNetStructure{
        ArrayList<PetriSim> list = new ArrayList<>();
        list.add(new PetriSim(NetLibrary.CreateNetGenerator(40.0, 1, "exp")));

        list.add(new PetriSim(NetLibrary.robotTakingAction(1, 1, Integer.toString(1)))); 
        list.add(new PetriSim(NetLibrary.robotTransportingAction(1, 6, Integer.toString(1))));
        list.add(new PetriSim(NetLibrary.robotPutAction(1, 1, Integer.toString(1))));
        list.add(new PetriSim(NetLibrary.robotTransportingAction(1, 1, "First comeback"))); 
        list.add(new PetriSim(NetLibrary.firstStation(60)));

        list.get(0).getNet().getListP()[1] = list.get(1).getNet().getListP()[0];
        list.get(1).getNet().getListP()[2] = list.get(2).getNet().getListP()[0];
        list.get(2).getNet().getListP()[1] = list.get(3).getNet().getListP()[0];
        list.get(1).getNet().getListP()[1] = list.get(4).getNet().getListP()[1];
        list.get(3).getNet().getListP()[1] = list.get(5).getNet().getListP()[0];

        list.add(new PetriSim(NetLibrary.robotTakingAction(1, 1, Integer.toString(2))));
        list.add(new PetriSim(NetLibrary.robotTransportingAction(1, 7, Integer.toString(2)))); 
        list.add(new PetriSim(NetLibrary.robotPutAction(1, 1, Integer.toString(2)))); 
        list.add(new PetriSim(NetLibrary.robotTransportingAction(1, 1, "Second comeback")));
        list.add(new PetriSim(NetLibrary.secondStation(100))); // station2 10
        list.add(new PetriSim(NetLibrary.robotTransportingBackAction(1, 1, "Line Change first")));
        
        list.get(6).getNet().getListP()[1] = list.get(11).getNet().getListP()[0];
        list.get(3).getNet().getListP()[2] = list.get(6).getNet().getListP()[1];
        list.get(5).getNet().getListP()[1] = list.get(6).getNet().getListP()[0];
        list.get(6).getNet().getListP()[2] = list.get(7).getNet().getListP()[0];
        list.get(7).getNet().getListP()[1] = list.get(8).getNet().getListP()[0];
        list.get(8).getNet().getListP()[2] = list.get(9).getNet().getListP()[0];
        list.get(6).getNet().getListP()[1] = list.get(9).getNet().getListP()[1];
        list.get(8).getNet().getListP()[1] = list.get(10).getNet().getListP()[0];
        list.get(11).getNet().getListP()[1] = list.get(4).getNet().getListP()[0];

        list.add(new PetriSim(NetLibrary.robotTakingAction(1, 1, Integer.toString(3)))); 
        list.add(new PetriSim(NetLibrary.robotTransportingAction(1, 5, Integer.toString(3))));
        list.add(new PetriSim(NetLibrary.robotPutAction(1, 1, Integer.toString(3))));
        list.add(new PetriSim(NetLibrary.robotTransportingAction(1, 1, "Third comeback")));
        list.add(new PetriSim(NetLibrary.robotTransportingBackAction(1, 1, "Line Change second")));
        
        list.get(12).getNet().getListP()[1] = list.get(16).getNet().getListP()[0];
        list.get(8).getNet().getListP()[2] = list.get(12).getNet().getListP()[1];
        list.get(10).getNet().getListP()[1] = list.get(12).getNet().getListP()[0];
        list.get(12).getNet().getListP()[2] = list.get(13).getNet().getListP()[0];
        list.get(13).getNet().getListP()[1] = list.get(14).getNet().getListP()[0];
        list.get(14).getNet().getListP()[2] = list.get(15).getNet().getListP()[0];
        list.get(12).getNet().getListP()[1] = list.get(15).getNet().getListP()[1];
        list.get(16).getNet().getListP()[1] = list.get(9).getNet().getListP()[0];


        PetriObjModel model = new PetriObjModel(list);
        return model;
    }

    public static PetriObjModel busStationModel(int peopleToRide) throws ExceptionInvalidTimeDelay, ExceptionInvalidNetStructure{
        int waitForPassangers = peopleToRide;
        ArrayList<PetriSim> list = new ArrayList<>();
        list.add(new PetriSim(NetLibrary.CreateNetGenerator(0.5, 1, "unif")));
        list.add(new PetriSim(NetLibrary.busStationCreation(0, waitForPassangers)));
        list.get(0).getNet().getListP()[1] = list.get(1).getNet().getListP()[0];

        PetriObjModel model = new PetriObjModel(list);
        return model;
    }

}
