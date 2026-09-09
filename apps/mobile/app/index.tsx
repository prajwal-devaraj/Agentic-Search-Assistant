import { useState } from "react";
import { ActivityIndicator, Pressable, SafeAreaView, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";

const API = process.env.EXPO_PUBLIC_PRAJNA_API_URL ?? "http://localhost:8000";
const modes = ["quick", "deep", "compare", "code", "news"] as const;
type Mode = typeof modes[number];

type Result = {
  answer: string;
  trust: { score: number; band: string };
  sources: { id: string; title: string; domain: string; snippet: string; score: number }[];
};

export default function Home() {
  const [query, setQuery] = useState("");
  const [mode, setMode] = useState<Mode>("quick");
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);

  async function search() {
    if (query.trim().length < 2 || loading) return;
    setLoading(true);
    try {
      const response = await fetch(`${API}/v1/search`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ query, mode, max_sources: mode === "deep" ? 10 : 6 }),
      });
      setResult(await response.json());
    } finally { setLoading(false); }
  }

  return (
    <SafeAreaView style={s.safe}>
      <ScrollView contentContainerStyle={s.page} keyboardShouldPersistTaps="handled">
        <View style={s.brandRow}><View style={s.mark}><Text style={s.markText}>P</Text></View><View><Text style={s.brand}>PRAJNA</Text><Text style={s.muted}>universal agentic search</Text></View></View>
        <Text style={s.kicker}>EVIDENCE BEFORE ELOQUENCE</Text>
        <Text style={s.title}>Ask anything.
See what supports it.</Text>
        <TextInput value={query} onChangeText={setQuery} placeholder="Research, compare, code, investigate…" placeholderTextColor="#596173" multiline style={s.input} />
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={s.modeRow}>
          {modes.map((m) => <Pressable key={m} onPress={() => setMode(m)} style={[s.mode, mode === m && s.modeActive]}><Text style={[s.modeText, mode === m && s.modeTextActive]}>{m}</Text></Pressable>)}
        </ScrollView>
        <Pressable onPress={search} style={s.search}><Text style={s.searchText}>{loading ? "Working…" : "Search"}</Text></Pressable>
        {loading && <ActivityIndicator color="#8bf0c4" style={{ marginTop: 25 }} />}
        {result && !loading && <View style={s.results}>
          <View style={s.scoreRow}><View><Text style={s.label}>TRUST</Text><Text style={s.score}>{result.trust.score}<Text style={s.scoreSmall}>/100</Text></Text></View><Text style={s.band}>{result.trust.band} evidence</Text></View>
          <View style={s.card}><Text style={s.label}>SYNTHESIS</Text><Text style={s.answer}>{result.answer}</Text></View>
          <Text style={s.section}>Sources</Text>
          {result.sources.map((source, i) => <View style={s.card} key={source.id}><Text style={s.sourceMeta}>{String(i+1).padStart(2,"0")}  ·  {source.domain}  ·  {Math.round(source.score*100)}%</Text><Text style={s.sourceTitle}>{source.title}</Text><Text style={s.muted}>{source.snippet}</Text></View>)}
        </View>}
      </ScrollView>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  safe:{flex:1,backgroundColor:"#090b10"},page:{padding:22,paddingBottom:70},brandRow:{flexDirection:"row",alignItems:"center",gap:11,marginTop:8,marginBottom:50},mark:{width:38,height:38,borderRadius:12,borderWidth:1,borderColor:"#3d6a5a",alignItems:"center",justifyContent:"center"},markText:{color:"#8bf0c4",fontWeight:"800",fontSize:18},brand:{color:"#f5f7fb",fontWeight:"800",letterSpacing:2},muted:{color:"#8f98aa",fontSize:12,lineHeight:18},kicker:{color:"#8bf0c4",fontSize:10,letterSpacing:2,marginBottom:10},title:{color:"white",fontWeight:"700",fontSize:38,lineHeight:43,letterSpacing:-1.3,marginBottom:25},input:{minHeight:120,borderRadius:16,borderWidth:1,borderColor:"#252b38",backgroundColor:"#10131a",color:"white",fontSize:16,padding:16,textAlignVertical:"top"},modeRow:{gap:8,paddingVertical:13},mode:{paddingVertical:7,paddingHorizontal:11,borderRadius:20,borderWidth:1,borderColor:"#252b38"},modeActive:{backgroundColor:"#181b2b",borderColor:"#515b93"},modeText:{color:"#727b8e",fontSize:11,textTransform:"uppercase"},modeTextActive:{color:"#aeb8ff"},search:{backgroundColor:"white",borderRadius:12,padding:14,alignItems:"center"},searchText:{color:"#090b10",fontWeight:"800"},results:{marginTop:28,gap:12},scoreRow:{flexDirection:"row",alignItems:"center",justifyContent:"space-between",marginBottom:3},label:{color:"#747d91",fontSize:10,letterSpacing:2},score:{color:"white",fontSize:46,fontWeight:"700",letterSpacing:-2},scoreSmall:{fontSize:12,color:"#747d91",letterSpacing:0},band:{color:"#8bf0c4",fontSize:11,textTransform:"uppercase"},card:{borderRadius:15,borderWidth:1,borderColor:"#222733",backgroundColor:"#10131a",padding:17},answer:{color:"#e7eaf1",fontSize:15,lineHeight:24,marginTop:12},section:{color:"white",fontSize:22,fontWeight:"700",marginTop:15,marginBottom:3},sourceMeta:{color:"#8bf0c4",fontSize:9,letterSpacing:1,marginBottom:8},sourceTitle:{color:"white",fontWeight:"700",fontSize:15,lineHeight:20,marginBottom:7}
});
