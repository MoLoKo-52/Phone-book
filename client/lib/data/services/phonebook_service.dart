import 'package:client/data/services/grpc_service.dart';
import 'package:client/domain/src/phonebook.pbgrpc.dart';

class PhonebookService {
  late PhonebookServiceClient phonebookServiceClient;

  Future<void> init() async {
    phonebookServiceClient = PhonebookServiceClient(
      await GrpcService().createChannel(),
    );
  }

  PhonebookServiceClient getPhonebookClient() {
    return phonebookServiceClient;
  }
}
