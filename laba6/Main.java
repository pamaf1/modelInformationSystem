import PetriObj.PetriObjModel;
import PetriObj.PetriSim;
import LibNet.NetLibrary;
import PetriObj.ExceptionInvalidTimeDelay;
import PetriObj.ExceptionInvalidNetStructure;
import java.util.ArrayList;
import PetriObj.PetriP;
import PetriObj.ArcIn;
import PetriObj.ArcOut;
import PetriObj.PetriT;
import PetriObj.PetriNet;

public class Main {

    public static void main(String args[]) {
        double timeModeling = 1000;
            try {
            PetriObjModel model = serverModel();
            model.go(timeModeling);
            model.printStatistics();
        } catch(Exception ex) {
            System.out.println(ex);
        }
    }

    public static PetriNet conveyorSystemBlock(int travel_time, String name) throws ExceptionInvalidTimeDelay, ExceptionInvalidNetStructure{
        ArrayList<PetriP> d_P = new ArrayList<>();
	    ArrayList<PetriT> d_T = new ArrayList<>();
	    ArrayList<ArcIn> d_In = new ArrayList<>();
	    ArrayList<ArcOut> d_Out = new ArrayList<>();
        d_P.add(new PetriP("P1",0));
        d_P.add(new PetriP("P3",0));
        d_T.add(new PetriT("T2", travel_time));
        d_T.get(0).setDistribution("exp", d_T.get(0).getTimeServ());
        d_T.get(0).setParamDeviation(0.0);
        

        d_In.add(new ArcIn(d_P.get(0), d_T.get(0), 1));

        d_Out.add(new ArcOut(d_T.get(0), d_P.get(1), 1));
        PetriNet d_Net = new PetriNet(name, d_P, d_T, d_In, d_Out);
        PetriP.initNext();
        PetriT.initNext();
        ArcIn.initNext();
        ArcOut.initNext();

        return d_Net;
    }

    public static PetriObjModel conveyorSystem() throws ExceptionInvalidTimeDelay, ExceptionInvalidNetStructure{
        ArrayList<PetriSim> list = new ArrayList<>();
        list.add(new PetriSim(NetLibrary.CreateNetGenerator(1.0, 4, "exp")));

        list.add(new PetriSim(conveyorSystemBlock(1, "Block 0")));
        list.add(new PetriSim(NetLibrary.CreateNetSMOwithoutQueue(1, 1, Integer.toString(0))));
        list.get(1).getNet().getListP()[0] = list.get(2).getNet().getListP()[0];
        list.get(0).getNet().getListP()[1] = list.get(1).getNet().getListP()[0];

        list.add(new PetriSim(conveyorSystemBlock(1, "Block 1")));
        list.add(new PetriSim(NetLibrary.CreateNetSMOwithoutQueue(1, 1, Integer.toString(1))));
        list.get(3).getNet().getListP()[0] = list.get(1).getNet().getListP()[1];
        list.get(4).getNet().getListP()[0] = list.get(3).getNet().getListP()[0];

        list.add(new PetriSim(conveyorSystemBlock(1, "Block 2")));
        list.add(new PetriSim(NetLibrary.CreateNetSMOwithoutQueue(1, 1, Integer.toString(2))));
        list.get(5).getNet().getListP()[0] = list.get(3).getNet().getListP()[1];
        list.get(6).getNet().getListP()[0] = list.get(5).getNet().getListP()[0];

        list.add(new PetriSim(conveyorSystemBlock(5, "Block 3"))); 
        list.add(new PetriSim(NetLibrary.CreateNetSMOwithoutQueue(1, 1, Integer.toString(3))));
        list.get(7).getNet().getListP()[0] = list.get(5).getNet().getListP()[1];
        list.get(8).getNet().getListP()[0] = list.get(7).getNet().getListP()[0];

        list.get(7).getNet().getListP()[1] = list.get(1).getNet().getListP()[0];

        PetriObjModel model = new PetriObjModel(list);
        return model;
    }

    public static PetriObjModel shopFridgeModel() throws ExceptionInvalidTimeDelay, ExceptionInvalidNetStructure{
        ArrayList<PetriSim> list = new ArrayList<>();

        list.add(new PetriSim(NetLibrary.CreateNetGenerator(0.2, 1, "exp")));
        list.add(new PetriSim(NetLibrary.CreateShopFridge())); 
        list.get(0).getNet().getListP()[1] = list.get(1).getNet().getListP()[0];
        
        PetriObjModel model = new PetriObjModel(list);
        return model;
    }

    public static PetriObjModel serverModel() throws ExceptionInvalidTimeDelay, ExceptionInvalidNetStructure{
        ArrayList<PetriSim> list = new ArrayList<>();
        list.add(new PetriSim(NetLibrary.CreateNetGenerator(1, 1, "exp")));
        list.add(new PetriSim(serverCreation(1, 0.4, "Server", 1.0f))); 
        list.add(new PetriSim(serverCreation(1, 0.6, "ReserveServer", 0.3f))); 

        list.get(1).getNet().getListP()[0] = list.get(2).getNet().getListP()[0];
        list.get(0).getNet().getListP()[1] = list.get(2).getNet().getListP()[0];
        
        PetriObjModel model = new PetriObjModel(list);
        return model;
    } 

    public static PetriNet serverCreation(int numChannel, double timeMean, String name, float prob) throws ExceptionInvalidNetStructure, ExceptionInvalidTimeDelay{
        ArrayList<PetriP> d_P = new ArrayList<>();
        ArrayList<PetriT> d_T = new ArrayList<>();
        ArrayList<ArcIn> d_In = new ArrayList<>();
        ArrayList<ArcOut> d_Out = new ArrayList<>();

        d_P.add(new PetriP("P1",0));
        d_P.add(new PetriP("P2",numChannel));
        d_P.add(new PetriP("P3",0));
        d_T.add(new PetriT("T1",timeMean));

        d_T.get(0).setDistribution("exp", d_T.get(0).getTimeServ());
        d_T.get(0).setParamDeviation(0.0);
        d_T.get(0).setProbability(prob);

        d_In.add(new ArcIn(d_P.get(0),d_T.get(0),1));
        d_In.add(new ArcIn(d_P.get(1),d_T.get(0),1));
        d_Out.add(new ArcOut(d_T.get(0),d_P.get(1),1));
        d_Out.add(new ArcOut(d_T.get(0),d_P.get(2),1));

        PetriNet d_Net = new PetriNet(name,d_P,d_T,d_In,d_Out);
        PetriP.initNext();
        PetriT.initNext();
        ArcIn.initNext();
        ArcOut.initNext();

        return d_Net;
    }
}
