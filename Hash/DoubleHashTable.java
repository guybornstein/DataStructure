import java.util.Random;

public class DoubleHashTable extends OAHashTable {

	private ModHash func1, func2;
	
	public DoubleHashTable(int m, long p) {
		super(m);
		this.func1 = ModHash.GetFunc(m, p);
		this.func2 = ModHash.GetFunc(m-2, p);
	}
	
	@Override
	public int Hash(long x, int i) {
		return (int)((((long)(this.func1.Hash(x)) + (long)i * (long)(1+this.func2.Hash(x)))) % this.size);
	}
	
}
