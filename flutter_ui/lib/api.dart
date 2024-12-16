import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

Future<String> predictSMS(String text) async {
  final url = Uri.parse((Platform.isAndroid) ? 'http://10.0.2.2:5000/predict' : 'http://127.0.0.1:5000/predict');
  final response = await http.post(
    url,
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'text': text}),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    return data['prediction'];
  } else {
    throw Exception('Failed to predict');
  }
}
