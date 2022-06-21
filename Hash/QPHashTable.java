import java.util.Random;

public class QPHashTable extends OAHashTable {

	private ModHash func;


	public QPHashTable(int m, long p) {
		super(m);
		this.func = ModHash.GetFunc(m, p);
	}
	
	@Override
	public int Hash(long x, int i) {
		return (func.Hash(x) + i^2) % this.size;
	}
}
